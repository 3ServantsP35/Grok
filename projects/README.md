# #mstr-cio Project Tracker
**Managed by:** Gavin (rizenshine5359) — Project Manager  
**Updated:** 2026-04-22

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
| P-AB1AB2-AUTO | Automating AB1 and AB2 Trading | 🟡 Active | Greg/Gavin/CIO |
| P-MCP-CSV | Automating CSV Uploads with MCP | 🟡 Active | Greg/Gavin/CIO |

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
| Define AB3 objective and relation to AB4 benchmark | ⬜ Planned |
| Formalize LEAP vs shares decision rules | ⬜ Planned |
| Define allowable overexposure conditions and limits | ⬜ Planned |
| Tie AB3 rules into PPR and branch-specific deployment logic | ⬜ Planned |

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
