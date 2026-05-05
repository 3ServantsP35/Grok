# #mstr-cio Project Tracker
**Managed by:** Gavin (rizenshine5359) — Project Manager  
**Updated:** 2026-05-01

---

## Project Status Summary

| Project | Name | Status | Owner |
|---|---|---|---|
| P-DOI | Distribution Signal Layer (Momentum assets) | 🟡 Active | CIO |
| P-MR-ENTRY | Cross-Asset LEAP Opportunity Framework | 🟡 Active | CIO |
| P-MSTR-SUITE | MSTR Chart Suite / MSTR Suite | 🟡 Active | Gavin/CIO |
| P-FF | Force Field / Force Field ROC | 🟡 Active | CIO |
| P-LAYER-ARCH | Layer Architecture Hardening | 🔴 HIGH | Gavin/CIO |
| P-ONBOARD-ARCH | Gavin Onboarding to Technical Architecture | 🟡 Active | Gavin/CIO |
| P-AB4-STRAT | Define the AB4 Strategy | 🔴 HIGH | Gavin/CIO |
| P-AB3-RULESET | Define the AB3 Ruleset | 🔴 HIGH | Gavin/CIO |
| P-SOUNDBOARD | Soundboarding Template / PPR Decision Workflow | 🟡 Active | Gavin/CIO |
| P-COUNCIL | Capital Allocation Council / Adversarial Decision Council | 🟡 Active | Gavin/CIO |
| P-OPT-SCREENER | Technical Options Opportunity Screener | 🟡 Active | Gavin/CIO |
| P-REPORTING | Portfolio and Layer Reporting Framework | 🟡 Active | Gavin/CIO |
| P-SERVICE-MODEL | Portfolio Strategy Service Model | 🔴 HIGH | Gavin/CIO |
| P-AB1AB2-AUTO | Automating AB1 and AB2 Trading | 🟡 Active | Greg/Gavin/CIO |
| P-MCP-CSV | Automating CSV Uploads with MCP | 🔴 HIGH | Greg/Gavin/CIO |

---

## Active Projects

---

### P-DOI: Distribution Signal Layer *(Momentum assets only)*
**Status:** 🟡 Active  
**Lead:** CIO | **Approver:** Gavin

Purpose: maintain and extend the purpose-built distribution signal layer for momentum assets where empirical validation is strong enough to justify dedicated distribution logic.

**Current scope:**
- maintain DOI signal quality for Momentum assets
- improve integration with trim / exit decision support
- keep non-momentum assets explicitly out of scope unless new evidence justifies expansion

**Next milestones:**
| Milestone | Status |
|---|---|
| Refine DOI signal interpretation for Momentum assets | 🟡 In progress |
| Wire DOI outputs more directly into CRS / trim-zone precision | ⬜ Planned |
| Reconfirm empirical scope boundaries by asset class | ⬜ Planned |

---

### P-MR-ENTRY: Cross-Asset LEAP Opportunity Framework
**Status:** 🟡 Active  
**Lead:** CIO | **Approver:** Gavin

Purpose: define high-confidence LEAP entry logic across the in-scope universe so the system is not overly dependent on MSTR-specific opportunity windows.

**Current scope:**
- asset-specific high-confidence entry windows
- cross-asset opportunity alignment
- methodology for validating LEAP entry conditions by asset class

**Next milestones:**
| Milestone | Status |
|---|---|
| Finish asset-specific signal specs | 🟡 In progress |
| Formalize episode taxonomy | ⬜ Planned |
| Extend and revalidate cross-asset backtest methodology | ⬜ Planned |

---

### P-MSTR-SUITE: MSTR Chart Suite / MSTR Suite
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: maintain the force-aware MSTR path dashboard and associated MSTR-specific reporting stack as the dedicated branch toolset for MSTR analysis.

**Current scope:**
- keep MSTR suite aligned with current branch architecture
- maintain documentation and live-path validation
- ensure suite outputs remain usable by downstream portfolio workflows

**Next milestones:**
| Milestone | Status |
|---|---|
| Confirm next live-path validation cycle | ⬜ Planned |
| Align suite outputs with current routing / branch language | ⬜ Planned |
| Preserve dashboard usefulness as AB and branch doctrine evolves | ⬜ Planned |

---

### P-FF: Force Field / Force Field ROC
**Status:** 🟡 Active  
**Lead:** CIO

Purpose: preserve Force Field as the structural state read and FF ROC as the primary tactical read for MSTR and related decision support.

**Current scope:**
- maintain FF ROC as primary tactical interpretation layer
- validate live usefulness against continuation / rejection behavior
- keep repo-first indicator maintenance discipline

**Next milestones:**
| Milestone | Status |
|---|---|
| Continue live validation of FF ROC behavior | 🟡 In progress |
| Decide long-term role of legacy FF display | ⬜ Planned |
| Keep docs and exports aligned with live interpretation rules | ⬜ Planned |

---

### P-LAYER-ARCH: Layer Architecture Hardening
**Status:** 🔴 HIGH  
**Lead:** Gavin/CIO

Purpose: harden the evolving SRI engine architecture, especially the Layer 0 through Layer 3 design, branch routing logic, Howell integration, AB doctrine, and document-level specification quality.

**Current scope:**
- stabilize the architecture described in the SRI Engine tutorial series
- convert architecture concepts into durable doctrine instead of ad hoc discussion
- tighten relationships among Howell phases, branch routing, AB posture, and PPR

**Initial milestones:**
| Milestone | Status |
|---|---|
| Harden Layer 0.5 Howell transition framework | ✅ v3.2.1 complete |
| Harden AB4 benchmark doctrine and PPR deviation logic | ✅ v3.2.2 complete |
| Formalize Howell transition marker matrix | ⬜ Next |
| Clarify branch-to-bucket implementation rules | ⬜ Planned |
| Continue architecture versioning discipline | 🟡 Ongoing |

---

### P-ONBOARD-ARCH: Gavin Onboarding to Technical Architecture
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: guide Gavin through professional development in technical architecture, especially the way Greg and Archie work, including building effectively with Claude and complementary tools.

**Current scope:**
- architectural thinking and systems decomposition
- tool-assisted design workflows
- prompt, planning, and review discipline for professional build work
- learning the operating style behind Greg’s build process

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define onboarding curriculum / sequence | ⬜ Planned |
| Map Greg/Archie workflow into teachable modules | ⬜ Planned |
| Create hands-on exercises tied to active MSTR-CIO work | ⬜ Planned |
| Track skill acquisition and gaps over time | ⬜ Planned |

---

### P-AB4-STRAT: Define the AB4 Strategy
**Status:** 🔴 HIGH  
**Lead:** Gavin/CIO

Purpose: define the AB4 strategy based on the scope clarified in SRI Engine v3.2.2, where AB4 is both base capital and the benchmark capital posture for the portfolio.

**Current scope:**
- formal AB4 benchmark doctrine
- Howell-driven benchmark posture rules
- reserve, ballast, diversification, and patience rules
- relation between benchmark posture and personalized deviation

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define AB4 benchmark architecture from v3.2.2 | ⬜ Planned |
| Specify benchmark outputs by Howell phase / transition state | ⬜ Planned |
| Define allowed owner deviation framework via PPR | ⬜ Planned |
| Identify implementation requirements for portfolio reporting | ⬜ Planned |

---

### P-AB3-RULESET: Define the AB3 Ruleset
**Status:** 🔴 HIGH  
**Lead:** Gavin/CIO

Purpose: define the AB3 ruleset for leverage through LEAPs and for share-based overexposure relative to the AB4 prescribed asset allocation benchmark.

**Current scope:**
- when LEAPs are appropriate vs when shares are appropriate
- when overexposure is allowed relative to AB4 benchmark posture
- how conviction, timing, and macro posture should constrain AB3
- documentation of acceptable deviation vs excessive risk

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define AB3 objective and relation to AB4 benchmark | 🟡 Drafted |
| Formalize LEAP vs shares decision rules | 🟡 Drafted |
| Define allowable overexposure conditions and limits | 🟡 Drafted |
| Tie AB3 rules into PPR and branch-specific deployment logic | 🟡 Drafted |

---
### P-SOUNDBOARD: Soundboarding Template / PPR Decision Workflow
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: define the soundboarding template and decision workflow used inside PPR channels so benchmark posture, deviation proposals, rationale, and final classifications are handled consistently.

**Current scope:**
- benchmark recommendation presentation
- deviation proposal workflow
- rationale capture and tradeoff discussion
- final posture classification and next-action framing

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define standard soundboarding template | ⬜ Planned |
| Define benchmark-aligned / acceptable deviation / owner override workflow | ⬜ Planned |
| Integrate template into PPR channel process | ⬜ Planned |
| Define what gets recorded vs what stays conversational | ⬜ Planned |

---

### P-COUNCIL: Capital Allocation Council / Adversarial Decision Council
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: build a structured multi-perspective council that pressure-tests capital allocation decisions before commitment, so the system gets better at challenging its own assumptions, reducing gas-lighting dynamics, and resisting groupthink.

**Current scope:**
- define a reusable council workflow for high-leverage capital decisions
- formalize distinct advisor roles rather than one blended assistant voice
- force explicit downside, first-principles, upside, outsider, and execution review before verdict
- integrate the council into layer-aware allocation and soundboarding decisions
- capture where the council agrees, where it clashes, and what blind spots it surfaces

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define the five-advisor council structure and chairman verdict format | ⬜ Planned |
| Map council lenses into AB4, AB3, Howell, and branch decision workflows | ⬜ Planned |
| Create prompts/templates for stress-testing major allocation decisions | ⬜ Planned |
| Define when to invoke council review vs normal soundboarding | ⬜ Planned |
| Design lightweight recordkeeping for disagreements, blind spots, and final verdicts | ⬜ Planned |

**Design note:**
- intended structure reflects a five-advisor council:
  - **Contrarian** for fatal-flaw / downside attack
  - **First Principles** for assumption stripping and reframing
  - **Expansionist** for upside / underappreciated optionality
  - **Outsider** for fresh-eyes pattern detection
  - **Executor** for practical feasibility and sequencing
- output should end with a **chairman’s verdict** that summarizes agreement, conflict, blind spots, and final recommendation
- this project is for **high-leverage decisions**, not trivial lookups or simple yes/no requests

---

### P-OPT-SCREENER: Technical Options Opportunity Screener
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: build a technical-analysis-driven screener for identifying opportunistic options entries where structure, timing, and asymmetry justify deeper review for AB1, AB2, or AB3 deployment.

**Current scope:**
- define the technical conditions that make an options entry worth surfacing
- scan the in-scope asset universe for high-quality setups rather than relying on ad hoc chart review
- rank candidate entries by timing quality, asymmetry, and regime compatibility
- separate income-oriented setups from directional-convexity setups
- feed the best candidates into soundboarding, council review, or trade-planning workflows

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define screener objective and in-scope option opportunity types | ⬜ Planned |
| Define technical trigger set for opportunistic entries | ⬜ Planned |
| Map triggers into AB1 / AB2 / AB3 candidate categories | ⬜ Planned |
| Design ranking logic for setup quality and asymmetry | ⬜ Planned |
| Prototype screener output format and review workflow | ⬜ Planned |

**Design note:**
- this project is about **finding technically attractive options entries**, not executing trades automatically
- it should remain distinct from **P-AB1AB2-AUTO**, which is about execution workflow and automation boundaries
- the screener should eventually help surface:
  - bullish income setups
  - bearish income setups
  - bullish convexity setups
  - bearish convexity setups
  - timing-sensitive MSTR-complex opportunities

---

### P-REPORTING: Portfolio and Layer Reporting Framework
**Status:** 🟡 Active  
**Lead:** Gavin/CIO

Purpose: define how the system reports on portfolios and layers so users can see benchmark posture, active deviations, branch state, and layer-by-layer reasoning in a coherent format.

**Current scope:**
- portfolio-level reporting
- layer-by-layer reporting
- benchmark vs actual posture visibility
- branch-aware and owner-aware reporting outputs

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define reporting audiences and report types | ⬜ Planned |
| Define layer-by-layer reporting schema | ⬜ Planned |
| Define benchmark vs actual posture reporting | ⬜ Planned |
| Define how reporting consumes soundboarding outputs | ⬜ Planned |

---

### P-SERVICE-MODEL: Portfolio Strategy Service Model
**Status:** 🔴 HIGH  
**Lead:** Gavin/CIO

Purpose: build the service layer that turns the existing market, layer, and portfolio architecture into a usable educational portfolio-management workflow for named users.

**Current scope:**
- define portfolio strategy as the primary object of the service
- turn architecture outputs into user-facing reporting, approvals, execution plans, and performance workflows
- keep the service configurable rather than bespoke
- support one tier of users, with learning modules that level users up into effective use of the system
- use Gavin's live portfolio as the first live-fire design case once current layer testing is complete

**Current framing:**
- weekly cadence with event-driven engagement
- core loop: user inputs → system strategy → user approval → system execution plan → user execution confirmation → performance/adjustment loop
- target core artifacts: Portfolio Strategy Report, Execution Plan, learning modules, execution confirmation workflow

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define v1 service operating model and lifecycle | 🟡 In progress |
| Draft Portfolio Strategy Report schema | ⬜ Planned |
| Draft Execution Plan schema | ⬜ Planned |
| Define user input/config schema | ⬜ Planned |
| Define learning-module set (service use, layers, management model) | ⬜ Planned |
| Run live-fire design pass on Gavin portfolio intake and reporting flow | ⬜ Planned |

---

### P-AB1AB2-AUTO: Automating AB1 and AB2 Trading
**Status:** 🟡 Active  
**Lead:** Greg/Gavin/CIO

Purpose: automate the trading workflows associated with AB1 and AB2 once the architecture and rulesets are sufficiently stable.

**Current scope:**
- convert AB1 / AB2 logic into machine-executable workflows
- identify trigger, approval, guardrail, and routing requirements
- determine which parts can be automated vs which remain supervised

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define automation boundary for AB1 and AB2 | ⬜ Planned |
| Identify signal inputs and execution prerequisites | ⬜ Planned |
| Design approval / oversight flow | ⬜ Planned |
| Build phased automation roadmap | ⬜ Planned |

---

### P-MCP-CSV: Automating CSV Uploads with MCP
**Status:** 🟡 Active  
**Lead:** Greg/Gavin/CIO

Purpose: automate CSV upload workflows using MCP so data flows into the system with less manual handling and lower operational friction.

**Current scope:**
- define MCP-based CSV upload workflow
- reduce manual upload burden
- improve repeatability, governance, and monitoring of data ingestion

**Initial milestones:**
| Milestone | Status |
|---|---|
| Define target CSV upload workflow and MCP touchpoints | ⬜ Planned |
| Identify required schemas, validations, and failure handling | ⬜ Planned |
| Design automation path and operator workflow | ⬜ Planned |
| Prototype MCP-mediated upload process | ⬜ Planned |

---

## Archived Projects

The following projects are archived as part of the 2026-04-22 tracker reset. They may still contain useful history, but they are no longer active tracker priorities under the current architecture direction.

| Project | Name | Prior status |
|---|---|---|
| P1 | Allocation Bucket Framework (AB1/AB2/AB3/AB4) | Archived |
| P2 | Bear Indicators | Archived |
| P4 | RORO / Howell Phase Engine | Archived |
| P5 | Alerts & Automation (incl. UAA) | Archived |
| P6 | Multi-TF SRI / Concordance (LOI) | Archived |
| P7 | Framework Architecture | Archived |
| P8 | Pine Scripts — Mirror Layer | Archived |
| P9 | MSTR/IBIT Pair Trade | Archived |
| P10 | Trend Line Engine | Archived |
| P11 | STRC Spread Monitor | Archived |
| P12 | Python Decision Engine | Archived |
| P13 | Recommendation Performance Journal | Archived |
| P14 | Bearish Bias Indicator Suite | Archived |
| P-BEAR | Bearish Signal & Adjustment Architecture | Archived |
| P-HOWELL | Howell Phase Engine | Archived |
| P-CLASSIFIER | Stage 2 Continuation Classifier | Archived |
| P-GLI | GLI Engine (Layer 0) | Archived |
| P-MSR | Market Structure Reports | Archived |
| P-PPR | Personalized Portfolio Report | Archived |
| P-MOCK | Weekly Generic Portfolio Brief | Archived |
| P-TUTORIALS | Tutorial v2.5 + Layman's Guide | Archived |
| P-CRS | AB2 Call Ripeness Score v2 | Archived |
| P-PINE-GUIDE | Pine Indicator Tutorial Guide | Archived |
| P-BACKTEST | Stage Designation + Vol-Adaptive Research | Archived |
| P-PINE-V6 | Pine v6 Migration | Archived |
| P-TVI | TradingView Integration | Archived |

---

## Notes on the Reset

- This reset reflects the current re-architecture effort rather than a judgment that the archived work was valueless.
- Several archived projects have been absorbed conceptually into the new architecture-driven roadmap.
- The active tracker now emphasizes durable doctrine, branch-aware portfolio design, automation pathways, and onboarding into technical architecture.

## Recommended Sequencing and Dependency Map

### Recommended order
1. **P-MCP-CSV**
2. **P-AB4-STRAT**
3. **P-AB3-RULESET**
4. **P-SOUNDBOARD**
5. **P-COUNCIL**
6. **P-OPT-SCREENER**
7. **P-REPORTING**
8. **P-SERVICE-MODEL**
9. **P-AB1AB2-AUTO**

### Parallel tracks
- **P-LAYER-ARCH** continues in parallel because architecture hardening affects almost every downstream project.
- **P-ONBOARD-ARCH** continues in parallel because Gavin’s skill development should happen alongside the real project work, not after it.
- Existing active market-intelligence projects (**P-DOI**, **P-MR-ENTRY**, **P-MSTR-SUITE**, **P-FF**) continue as standing workstreams.

### Dependency logic
- **P-MCP-CSV → P-AB4-STRAT**
  - MCP/CSV automation is now treated as an enabling project because AB4 strategy work needs reliable, repeatable backtesting inputs.
- **P-AB4-STRAT → P-AB3-RULESET**
  - AB3 rules depend on a clear benchmark posture to define what counts as overexposure or justified deviation.
- **P-AB4-STRAT + P-AB3-RULESET → P-SOUNDBOARD**
  - the soundboarding workflow must know what the benchmark is and what deviation rules exist before it can guide users coherently.
- **P-SOUNDBOARD → P-COUNCIL**
  - the council should sit on top of a defined soundboarding workflow so adversarial review is structured rather than improvised.
- **P-SOUNDBOARD + settled technical doctrine → P-OPT-SCREENER**
  - the screener should surface candidates into an already-defined review vocabulary rather than inventing its own recommendation language.
- **P-OPT-SCREENER → P-REPORTING**
  - reporting should eventually show what opportunities were surfaced, why they ranked highly, and how they resolved.
- **P-REPORTING → P-SERVICE-MODEL**
  - the service layer should sit on top of the reporting layer so users can receive strategy recommendations, gap analysis, and execution guidance in a coherent operating model rather than as disconnected reports.
- **P-SERVICE-MODEL + settled doctrine → P-AB1AB2-AUTO**
  - automation should come after the system has stable benchmark language, deviation rules, reporting outputs, service workflows, and user-approval patterns.

### Interpretation
The architecture work has made doctrine the bottleneck, but the user-directed reprioritization means **data plumbing now becomes the first enabling step** because AB4 strategy needs backtesting support. The new council project adds an explicit anti-groupthink layer so major capital decisions are stress-tested before they become doctrine, recommendation, or automation. The new options screener project adds a dedicated technical funnel for surfacing higher-quality options entries before they reach execution or reporting layers.
