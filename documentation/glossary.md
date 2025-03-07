# Glossary

```{glossary}
:sorted:

action
policy action
intervention
measure
  Actions do not change often and are often used in multiple {term}`studies <study>`. Within
  a single study, actions are often part of multiple {term}`sequences <sequence>`.

  Examples:

  - Raise river embankment by `x` cm.
  - Room for the rivers by `x` ha.

sequence
action sequence
  A sequence of {term}`actions <action>`. Certain sequences can be useful in multiple
  {term}`studies <study>`.

  Examples:

  -
     ```{mermaid}
     flowchart LR
     room[room for rivers] --> raise[raise river embankment]
     ```

scenario
  Some condition that changes over time resulting in negative effects on the environment,
  including us. A {term}`pathways study <study>` helps to analyse possible ways to mitigate
  these effects. Scenarios can be used in multiple projects. A scenario is encoded as a
  time series.

  Examples:

  - Sea level rise.
  - The discharge of the Rhine increases with `x` m³ / sec per year.

tipping point
  A moment in time or a condition that will render an {term}`action` or a {term}`sequence
  of actions <sequence>` as ineffective. Tipping points are unique per {term}`study`. Under the
  same {term}`scenario` and applying the same actions often different tipping points have
  to be used, when applied to different regions of the world.

  Examples:

  - A certain embankment collapses when the discharge becomes higher than `x` m³ / sec.

pathway
adaptation pathway
  A combination of a {term}`sequence <sequence>`, a {term}`scenario <scenario>`, and
  {term}`tipping points <tipping point>`. Pathways are unique for a {term}`study`.
  Pathways can be visualized as {term}`pathway maps <pathway map>`.

pathway map
  TODO

study
pathway study
adaptation pathway study
  A study is an analysis of a set of {term}`adaptation pathways <pathway>`. This
  involves defining {term}`actions <action>`, combining them into multiple {term}`sequences
  <sequence>`, and adding information about a {term}`scenario` and {term}`tipping points
  <tipping point>`. This allows the pathways to be compared. Depending on the functionality
  of the pathway analysis software, various metrics can be calculated to aid in the comparison.
```
