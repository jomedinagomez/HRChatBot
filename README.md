# HR Search Demo

**Demo PDFs -> local notebook -> Content Understanding -> chunks and embeddings
-> Azure AI Search -> search tests.**

## Files

- [architecture](architecture): three diagrams, each with its dataflow and how every
  connection signs in: the customer's architecture moved to Azure AI Search and
  Copilot Studio, what this demo deploys, and a fully native Azure pipeline.
- [samples/documents](samples/documents): 23 fictional HR PDFs, laid out like the
  customer's S3 bucket, so the audience comes from the folder and never from text
  on the page:

  ```
  domain=hr_chatbot/src=<system>/persona=<manager|non-manager>/<file>.pdf
  ```

  - `src=policy_hub` — 12 formal policies (Times serif, navy, underlined numbered
    sections), including the four-page nationwide sick leave policy and five state
    supplements that repeat its answers.
  - `src=people_central` — 6 ServiceNow knowledge articles, named
    `Topic_Scope_PERSONA_KBnumber.pdf`. Two are manager-only.
  - `src=sharepoint` — 5 pages (Helvetica, purple): a benefits FAQ, a manager quick
    card, a memo, an eligibility matrix, and HR quick answers (scripted Q&A).
- [samples/metadata.json](samples/metadata.json): one record per document with
  `persona` (`Manager` or `Non-Manager`), the derived `group_ids` security filter
  value, the citation `url`, and `content_source`.
- [scripts/generate_samples.py](scripts/generate_samples.py): regenerates the whole
  corpus and `metadata.json`. Run it if you want to change the fictional facts.
- [infra](infra): Terraform for every Azure and Microsoft Entra resource, keyless. See
  [Run](#run). What Terraform can't deploy is done by notebooks 00 and 04.
- [00_publish_mock_workday.ipynb](notebooks/00_publish_mock_workday.ipynb): publish the
  mock Workday's code to the function app Terraform created, and check it.
- [01_process_pdfs.ipynb](notebooks/01_process_pdfs.ipynb): extract Markdown with
  Content Understanding, split by titles/sections, generate embeddings, and save JSON.
- [02_create_index.ipynb](notebooks/02_create_index.ipynb): create the vector index
  and semantic-ranker configuration. No document uploads.
- [03_populate_and_test_index.ipynb](notebooks/03_populate_and_test_index.ipynb):
  upload the JSON, then try keyword, vector, and semantic hybrid search as a fake
  employee or a fake manager.
- [04_deploy_copilot_studio.ipynb](notebooks/04_deploy_copilot_studio.ipynb): deploy the
  Copilot Studio agent that answers from the index with the same manager / employee
  trimming. See [Copilot Studio](#copilot-studio).
- [copilot_studio](copilot_studio): the HR knowledge topic and the Workday (mock)
  connector definition that notebook 04 deploys.
- [mock_workday](mock_workday): a small Azure Function standing in for Workday,
  protected by Microsoft Entra ID. It returns the caller's own worker record,
  including `isManager`, and lets you change anyone's role on the fly. See
  [Mock Workday](#mock-workday).

## What the demo covers

Scoped to what the customer asked to see. Their list for stakeholders was
*"citations, persona, scripted answers, and questions."*

| Ask | Where it shows up |
|---|---|
| Manager vs. non-manager content | 3 manager-only documents, trimmed by the `group_ids` security filter in notebook 03 and in Copilot Studio |
| Simulate a few fake employees | Your own identity, or one service principal per role; flip any of them with `set-role.ps1` |
| Workday tells the bot who is a manager | Copilot Studio calls the mock Workday on behalf of the signed-in user (Microsoft Entra OBO); notebook 03 calls it with your own token. Both pass `isManager` into the search filter |
| Citations back to the source | The document's link in its source system, in `url` on every chunk; see [Citations](#citations) |
| Scripted answers (Lex today) | `HR Quick Answers.pdf`, indexed like any other document |
| Same answer in several documents | The nationwide sick leave policy plus five state supplements |

Left out until the customer asks for them: filtering by state or country, PTO
eligibility, and document lifecycle (drafts, expiry, superseded versions). The
state supplements are here as *content* for the overlap problem, not as a filter.

## Document-level security

The index uses the [security filter pattern](https://learn.microsoft.com/azure/search/search-security-trimming-for-azure-search),
which is generally available and works with any API version or SDK:

- `group_ids` is a `Collection(Edm.String)`, **filterable** and **not retrievable**,
  holding the principals allowed to read each chunk.
- Queries trim with a single `group_ids/any(g: search.in(g, 'a|b|c', '|'))` clause.
  `search.in` stays subsecond with hundreds of principals, unlike a chain of `eq`
  comparisons; `any()` is needed because `group_ids` is a collection.
- In production those strings are Microsoft Entra group object IDs. The demo uses
  readable slugs so the audience can follow what is happening.

`group_ids` comes straight from the customer's own `persona` rule, where
`Non-Manager` means every employee can read the document:

| `persona` | `group_ids` |
|---|---|
| `Non-Manager` | `all-employees` |
| `Manager` | `managers` |

The role comes from the mock Workday, looked up by the caller's identity:

| Workday says | Groups passed | Documents visible |
|---|---|---|
| `isManager: false`, or unknown identity | `all-employees` | 20 |
| `isManager: true` | `all-employees`, `managers` | 23 |

This is string matching, not an authorization check. Whatever calls Search resolves
the caller's groups and is trusted to pass them honestly.

### Two things to confirm before promising this to a customer

**The native Copilot Studio connection does not apply it.** Copilot Studio's
Azure AI Search knowledge source offers four authentication types — Access Key,
Client Certificate, Service principal, and Microsoft Entra ID Integrated — and all
four authenticate the *connection* to the service. The knowledge configuration
takes an index name and nothing else: there is no place to inject an OData filter,
and the documentation does not describe the end user's token being forwarded. The
[copilot_studio](copilot_studio) topic gets around this by running the search
itself; see [Copilot Studio](#copilot-studio).

**The newer native ACL feature is still preview.** Azure AI Search also supports
[permission filters](https://learn.microsoft.com/azure/search/search-document-level-access-overview)
(`permissionFilter` on a field, `permissionFilterOption` on the index) that compare
real Entra principals from an `x-ms-query-source-authorization` token. That is a
stronger model, but as of this writing it is preview-only: it needs a preview REST
API and a beta SDK (`azure-search-documents` 11.6.0, pinned here, has no permission
filter types at all), and it still depends on the caller forwarding a user token,
which the native Copilot Studio connection does not do.

## Run

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
az login
terraform -chdir=infra init
terraform -chdir=infra apply      # set subscription_id in infra/terraform.tfvars first
```

[infra](infra) deploys everything with Terraform, keys turned off (Microsoft Entra ID
only), and writes `.env` with every endpoint and name the notebooks need:

- a Microsoft Foundry resource for Content Understanding, with two model deployments:
  **gpt-5.5**, the newest and largest model Content Understanding supports, and
  **text-embedding-3-large**;
- Azure AI Search, Basic tier with semantic ranker (about $75 a month while it exists),
  whose managed identity calls the embedding model to vectorize queries;
- the mock Workday (see [Mock Workday](#mock-workday)) and its two app registrations;
- a service principal the agent's search connection signs in as, which can only read
  the index;
- roles for you to use all of it.

`terraform destroy` removes everything. The state stays in `infra/` and holds the
connector's client secret, so it's git-ignored.

The notebooks do everything else. Open them in VS Code, select `.venv`, and run them in
order, cell by cell:

| Notebook | What it does |
|---|---|
| **00** | Publishes the mock Workday's code to the function app |
| **01 → 02 → 03** | Builds the index and tests it as a fake employee or manager |
| **04** | Deploys the Copilot Studio agent (see [Copilot Studio](#copilot-studio)) |

The notebooks load `.env`, which Terraform rewrites on every apply; to use resources
you already have, copy [.env.example](.env.example) to `.env` and fill it in instead.
Each notebook stands alone; intermediate data is saved under the ignored `output`
folder. Cells that publish, extract, embed, create the index, upload, search, or deploy
make real Azure calls and incur charges.

Every step is also a VS Code task (**Terminal > Run Task**, in order from
`1. Terraform` to `7. Notebook 04`), and `.\.venv\Scripts\ipython.exe notebooks\<name>.ipynb`
runs a notebook top to bottom in a terminal.

If `terraform apply` fails with *connection may have been reset* or *EOF*, a network
client that drops idle connections is in the way (Microsoft Global Secure Access did
here). Pause it, or simply rerun `terraform apply`: it picks up where it stopped.

There are no assertion suites, custom validation/retry routines, or offline/live
switches. SDK errors are shown normally in the notebook; upload failures are printed.
Review the Markdown and chunks before populating the index.

The Search service should have semantic ranker enabled. The index uses
`text-embedding-3-large`, 3072 dimensions, and a matching query vectorizer.
The notebook identity needs Search write/schema access and CU/model access;
Search's managed identity needs **Cognitive Services OpenAI User** on the model
resource for query vectorization.

Use a new index name for a fresh corpus/chunking experiment. Matching chunk IDs
are replaced on upload; this demo does not automatically remove older chunks.

The demo code follows these examples, without their surrounding application
scaffolding:

- [Traditional RAG processing](https://github.com/jomedinagomez/RAG_process/tree/main/Traditional_RAG)
- [Azure Search Python vector samples](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code)

## Copilot Studio

There are two ways to point an agent at the index:

| | Native knowledge source | Custom knowledge topic |
|---|---|---|
| How | **Add knowledge → Azure AI Search** | [`OnKnowledgeRequested`](https://learn.microsoft.com/microsoft-copilot-studio/guidance/custom-knowledge-sources) topic in [copilot_studio](copilot_studio) |
| Manager / employee trimming | No: every user sees every document | Yes: `group_ids/any(g: search.in(g, …))` on every search |
| Citations | `metadata_storage_path` | `url`, mapped to `ContentLocation` |
| Setup | No code | One script |

Use the native source to show the index works as-is, and the topic to show persona
trimming. Don't add both to the same agent: results from every knowledge source are
merged, so the native one would bring back what the topic filtered out.

### Deploy

[04_deploy_copilot_studio.ipynb](notebooks/04_deploy_copilot_studio.ipynb) builds the
agent with your Azure CLI sign-in. No keys anywhere: the mock Workday and Azure AI
Search both take Microsoft Entra tokens. It's a notebook rather than Terraform because
the Power Platform Terraform provider can't create a custom connector or publish an
agent. Before you run it:

- `terraform apply` has run, with `power_platform_environment_url` set in
  [terraform.tfvars](infra/terraform.tfvars) (your `az login` must be in the same tenant);
- notebooks 01–03 have built the index;
- the Power Platform CLI is installed and signed in to the same tenant, to package the
  agent: `dotnet tool install --global Microsoft.PowerApps.CLI.Tool`, then
  `pac auth create --environment https://<org>.crm.dynamics.com`. `pac` only builds the
  package on disk, but it prints the account it's signed in as.

Terraform already created the connector's app registration. On-behalf-of (OBO) means
Power Platform exchanges the signed-in user's token for one for the Workday API, and it
needs a client app of its own to do that. Following
[Microsoft's setup](https://learn.microsoft.com/microsoft-copilot-studio/advanced-custom-connector-on-behalf-of),
it asks for `Workers.Read` (admin-consented) and exposes `access_as_user` to Azure API
Connections. The notebook creates:

1. **The Workday (mock) custom connector** from
   [workday-connector](copilot_studio/workday-connector), with on-behalf-of login on.
   The app's client secret goes from Terraform's state straight into the connector and
   is never written to disk or shown.
2. **The agent, HR Assist,** with [hr-knowledge.topic.yaml](copilot_studio/hr-knowledge.topic.yaml),
   web search and general knowledge off. `pac` packages it on disk; Dataverse imports
   it. Everything sent to the environment goes as your `az` sign-in.
3. **The Azure AI Search connection**, signed in as the service principal Terraform
   created for it, which can only read the index (Search Index Data Reader). No one has
   to sign in to it by hand, and its secret goes straight from Terraform's state into
   the connection. Searches run as a service, the way their backend queries OpenSearch
   today; who sees which documents is still decided per user by the Workday filter.
4. **The two connection references** the topic uses, linked to the topic. Then it
   publishes the agent and shows the result.

The Workday (mock) connection is each user's own: the **Allow** card the first time
they ask a question creates it. For anyone else to use the agent, share the Workday
(mock) connector with them.

Rerun the notebook after changing the topic; it updates the same connector and agent.

### How it works

The topic runs on every knowledge request, in three steps:

1. **Workday (mock) – Get Profile**, as the signed-in user. Power Platform exchanges
   their token for one for the Workday API, and the mock reads who they are from it.
2. `isManager` becomes the filter: `group_ids/any(g: search.in(g, 'all-employees|managers', '|'))`
   for managers, `'all-employees'` for everyone else, including anyone Workday doesn't
   know and any failed call. It's built only from Workday's answer, never from the
   user's message.
3. **Azure AI Search – Semantic hybrid search** with that filter, over the read-only
   service principal connection, the way their backend queries OpenSearch as a service
   today. Copilot Studio writes the answer and cites `url`. It uses at most 15 results,
   so the topic asks for 10.

### Test it

Make yourself an employee with `.\mock_workday\set-role.ps1 employee` and ask "How do
I prepare for a performance calibration?" The manager calibration guide (KB0010537)
must not be cited. Run `set-role.ps1 manager` and ask again: now it is. Workday is
asked on every question, so a change shows on the next one.

The topic validates against Copilot Studio's published
[authoring schema](https://github.com/microsoft/skills-for-copilot-studio/blob/main/reference/bot.schema.yaml-authoring.json),
and `pac copilot pack` accepts it. The Power Fx, the connector calls and the sign-ins
only run once the agent is in your environment.

For production, swap the Workday (mock) connector for their Workday connector's
**Get Profile**: it uses the same Entra on-behalf-of sign-in, and `isManager` is
Workday's own field name, so the rest of the topic stays the same.

## Mock Workday

[mock_workday](mock_workday) is an Azure Function standing in for Workday, protected
by Microsoft Entra ID the way their Workday is (delegated OAuth, no keys):

- `GET /api/workers/me` returns the caller's own worker record (the caller is whoever
  their token says), or a 404 if Workday doesn't know them.
- `PUT /api/workers/{user}` adds a worker or changes a field such as `isManager`. It
  needs the **Workers.Admin** app role, which Terraform gives you and nobody else.

App Service authentication turns away anything without a valid token for the mock's
own app registration (`api://<WORKDAY_API_APP_ID>`) before the code runs. Users are
identified by user principal name, service principals by client ID. Records use the
field names of Workday's worker summary (`isManager`, `primaryWorkEmail`,
`businessTitle`, `primarySupervisoryOrganization`) and live in a storage table, so a
role changes immediately with no redeploy. The function reads the table with its own
managed identity; the storage account has shared keys turned off.

```powershell
.\mock_workday\set-role.ps1 manager          # you, as az is signed in
.\mock_workday\set-role.ps1 employee -User <user principal name or client ID>
```

Run `set-role.ps1` from PowerShell 7 (`pwsh`). Windows PowerShell 5.1 runs it too, but
its web calls can stall for minutes on some networks.

Terraform ([workday.tf](infra/workday.tf)) creates the storage account, a Flex
Consumption Function App with App Service authentication, and the API's app
registration: scope `Workers.Read`, app role `Workers.Admin`, and the Azure CLI
pre-authorized so `az` and the notebook can get tokens. It seeds the table from
[workers.json](mock_workday/workers.json) once; roles you change later stay as they
are. Notebook 00 publishes the code (see [Run](#run)).

### Run it locally

Terraform also writes `mock_workday/local.settings.json`, which points a local host at
the same table (read with your `az` login), so local and cloud runs see the same roles:

```powershell
cd mock_workday
py -3.12 -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
func start
```

Point notebook 03 at it by setting `WORKDAY_MOCK_URL=http://localhost:7071/api/workers/me`
in `.env`, and pass the same URL to `set-role.ps1 -Url`. `func start` has no App
Service authentication, so locally the function reads the token without validating
it; that code path never runs in Azure.

### Test with several identities

Notebook 03 runs the agent's three steps with the selected persona's credential: it
gets a token for the mock, calls `GET /workers/me`, and builds the filter from
`isManager`. Your own `az` sign-in needs nothing else. For a service principal, add a
`ClientSecretCredential` to `personas` and give it a role with
`set-role.ps1 -User <client id>`. Search always runs as the notebook's own credential,
like the agent's service principal connection.

## Citations

Every answer cites the documents it came from, with a link back to each one in its
source system. The link is the `url` field, and it travels like this:

| Step | Where | What happens |
|---|---|---|
| Source | [metadata.json](samples/metadata.json) | One `url` per document: its link in the system it lives in, like the source link in the customer's own metadata JSON. |
| Chunking | [notebook 01](notebooks/01_process_pdfs.ipynb) | Every chunk of a document gets the document's `url` (the same value also goes in `metadata_storage_path`), its `title`, and a `section_title` from the Markdown headings. Each chunk's `content` starts with the title and section path, so the model knows where a passage comes from. |
| Index | [notebook 02](notebooks/02_create_index.ipynb) | `url` and `metadata_storage_path` are stored as plain strings: returned with results, never searched. `title`, `section_title` and `content` are searchable. |
| Agent | [hr-knowledge.topic.yaml](copilot_studio/hr-knowledge.topic.yaml) | The search returns `title`, `content` and `url` for up to 10 chunks, and the topic hands them to Copilot Studio as citations; see below. |
| Test | [notebook 03](notebooks/03_populate_and_test_index.ipynb) | Prints the same `url` as `Citation:`, so you see locally what the agent would cite. |

### Where `url` becomes the citation

There's no citation setting in Copilot Studio or on the index. Three lines of
[hr-knowledge.topic.yaml](copilot_studio/hr-knowledge.topic.yaml) do it:

| Line | What it does |
|---|---|
| `selectFields: =["title", "content", "url"]` | Asks Search to return `url` with each chunk. |
| `url: String` (under `dynamicOutputSchema`) | Declares it in the search step's output, so the next step can read it. |
| `ContentLocation: ThisRecord.url, Title: ThisRecord.title` | **This one makes it the citation.** It fills `System.SearchResults`, the table Copilot Studio writes answers from. There, each result's `Content` is the text, `ContentLocation` its link and `Title` its name ([format](https://learn.microsoft.com/microsoft-copilot-studio/guidance/custom-knowledge-sources)). |

To cite a different field, point `ContentLocation` at it (and add it to the first two
lines).

### What Copilot Studio does with it

1. When a question needs knowledge, Copilot Studio runs the topic (its trigger is
   `OnKnowledgeRequested`), passing a rewrite of the question that takes the
   conversation into account (`System.SearchQuery`).
2. The topic puts up to 10 chunks in `System.SearchResults`. Copilot Studio uses up to
   15 per answer, across all knowledge topics combined.
3. The model writes the answer from those chunks' `Content` and adds in-text citations.
   The chat shows each one as a numbered reference: the chunk's `Title`, linking to its
   `ContentLocation`.
4. Our agent answers only from the index: notebook 04 turns off general knowledge
   (**Allow ungrounded responses**, in the agent's Generative AI settings). Copilot
   Studio then shows an answer only if it carries an in-text citation. If the model
   leaves the citation out, the agent withholds the answer and replies as though it
   found nothing; asking again usually works. Microsoft suggests making this rarer by
   adding to the agent's instructions: *"Always include an in-text citation to the
   source document for every statement."* Our agent has no instructions yet
   ([details](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio#why-the-agent-sometimes-doesnt-return-a-grounded-answer)).
5. Channels differ: Teams shows at most 20 citations per answer, with titles cut to
   about 80 characters. If you replace the answer with your own message or Adaptive
   Card, citations aren't added for you.

### Sample links

The links are shaped like the customer's real ones:

| Source | `url` |
|---|---|
| Policy Hub | `https://meridian.policyhub.com/PolicyHub/DocumentViewer.aspx?Document=1200&...` |
| People Central (ServiceNow) | `https://meridianexternal.service-now.com/hrportal?id=kb_article_view&sys_kb_id=...` |
| SharePoint | `https://meridianfg.sharepoint.com/sites/HRConnect/HR%20Help/HR%20Quick%20Answers.pdf` |

### Good to know

- **A citation opens the whole document, not the section**: all chunks of a document
  share one `url`. To land on a section, give each chunk its own deep link, if the
  source system has them.
- **Why the URL is stored twice:** our agent cites `url`. Copilot Studio's built-in
  Azure AI Search knowledge source (see [Copilot Studio](#copilot-studio)) picks its
  citation itself: `metadata_storage_path` when the index has it, otherwise
  [any field holding a full URL](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-azure-ai-search#return-citations).
  Keeping both makes either setup cite the same link.
- **A citation doesn't grant access.** The link opens in the source system with the
  user's own permissions, so users need access there too.
- **The sample links don't open**: they point at a fictional tenant so they look right
  in a demo. For clickable citations, put real links in `url` in
  [metadata.json](samples/metadata.json), then rerun notebooks 01 and 03.

All policies are fictional, not actual employer rules or legal advice. The private
`.docs` folder is never an input. There is no application framework, deployment
pipeline, Functions orchestrator, or cloud change-tracking implementation here.
