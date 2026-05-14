# Score Method for MI

Lu, K. & Guo, H. (2021). *Pharmaceutical Statistics*.

## Objectives

1. Understand the formula logic and code correspondence
2. Clarify its relationship with Lu (2008) and PharmaSUG 2025 macro
3. Boundary scenario robustness analysis

---

## Background

### Clinical Trial Scenario

- Two groups, binary endpoint (success/failure)
- Parameter: risk difference p₁ − p₂
- Possible stratification (center, region)
- Missing data → need Multiple Imputation (MI)

### Required Output

- Point estimate d̄ of risk difference
- 95% confidence interval (LCL, UCL)

> Core question: How to correctly construct score CI under MI framework?

---

## Method Overview

The Proposed Score Method adapts MN score method into MI framework:

1. For each imputed dataset, compute MN score statistic
2. Combine across imputations: d̄ = mean(d_j), B = var(d_j)
3. Use Rubin's rule for total variance: V(δ) = W̄(δ) + (1+1/m)·B
4. Solve CI via test inversion: { δ : |Z(δ)| ≤ z }

> Key innovation: combine MI results at the Z-statistic level, not at the CI or stderr level. This preserves the δ-dependent variance structure of the score method.

---

## Complete Data MN Score Method

CMH weights:

$$w_h^* = n_{1h} \cdot n_{2h} / (n_{1h} + n_{2h})$$

$$w_h = w_h^* / \sum w_h^*$$

Z statistic:

$$Z(\delta) = \frac{\sum_h w_h(\hat{p}_{1h} - \hat{p}_{2h} - \delta)}{\sqrt{\sum_h w_h^2 \cdot \tilde{V}_h(\delta)}}$$

Variance with finite population correction:

$$\tilde{V}_h(\delta) = \left[\frac{\tilde{p}_{1h}(1-\tilde{p}_{1h})}{n_{1h}} + \frac{\tilde{p}_{2h}(1-\tilde{p}_{2h})}{n_{2h}}\right] \cdot \frac{N_h}{N_h - 1}$$

> CI = { δ : |Z(δ)| ≤ z_{α/2} }. Variance V depends on δ through constrained MLE — this is NOT a Wald method.

### Three Key Components

- CMH weights: larger strata contribute more
- Constrained MLE: maximize likelihood under p̃₁ − p̃₂ = δ → solve via Cardano formula
- Finite population correction: N/(N−1) adjusts small-sample bias

---

## Constrained MLE via Cardano Formula

Given δ, solve for p̃₁, p̃₂ under constraint p̃₁ − p̃₂ = δ:

```python
# Quartic coefficients
a = theta + 1
b = (theta+2)*delta - (theta+1) - (theta*p1 + p2)
c = delta**2 - (theta+1+2*p2)*delta + theta*p1 + p2
d = p2 * delta * (1 - delta)

# Cardano formula
v = (b/(3*a))**3 - b*c/(6*a**2) + d/(2*a)
u = sign(v) * sqrt(b**2/(9*a**2) - c/(3*a))
w = (pi + arccos(v/u**3)) / 3

# Solve
p2_tilde = 2*u*cos(w) - b/(3*a)
p1_tilde = p2_tilde + delta
```

### Boundary Protection

| Risk | Protection |
|------|------------|
| u ≈ 0 | Set v/u³ to 0 |
| v/u³ > 1 | Clamp to [-1, 1] |
| p̃ outside [0,1] | min(1, max(0, p̃)) |
| V ≈ 0 | Return Z = 100 |

> Warning: The PharmaSUG 2025 macro lacks these protections — silently produces incorrect CI under 0%/100% scenarios.

---

## Method Comparison

| Method | MI Variance | CI Construction | Characteristic |
|--------|-------------|-----------------|----------------|
| Complete MN | N/A | Score inversion | Baseline (complete data) |
| LMB | Effective n | Wald | Simple but fails when x=0 |
| Proposed Score | Rubin: W̄+(1+1/m)B | Score inversion | Preserves δ-dependent variance |
| Wald-Rubin | Rubin: W̄+(1+1/m)B | Wald (d̄ ± t√T) | Simple but loses score advantage |

> Core distinction: Proposed Score combines at Z(δ) level (preserves score inversion), Wald-Rubin combines at CI level (degrades to Wald).

---

## Summary

1. Proposed Score Method combines MI results at Z(δ) level, preserving score inversion's δ-dependent variance structure
2. Cannot directly Rubin-combine Lu (2008) — MN variance depends on δ via constrained MLE
3. Boundary 0%/100% — PharmaSUG macro fails silently, this project has 4-layer protection

### Code Resources

| File | Purpose |
|------|---------|
| formulas.R | R core functions |
| simulation.R | Monte Carlo simulation |
| Proposed_Score_MI_SAS.sas | SAS MI implementation |
