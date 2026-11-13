# Identifying the Most Reliable Players Under Pressure
**RR SupeRR Selector, Season 2 · Round 1 Methodology Report** · [Team name]

*Data: IPL and T20I ball-by-ball records from 2022 onwards (200,961 deliveries, 867 matches). All figures below are computed from the supplied data by a deterministic pipeline (appendix).*

---

## 1. Executive summary and final rankings

We built a ball-level **Pressure Index (PI) ∈ [0, 1]** from the state of the match *before* each delivery, split deliveries into Low / Medium / High pressure bands, and measured every batter and bowler against (i) league peers facing the same kind of delivery and (ii) their own ordinary performance. Small samples are shrunk with empirical Bayes, and the final score blends pressure level (60%), improvement on the player's own baseline (25%) and match-by-match consistency (15%). The **Pressure rating** is `50 + 10·z`, so 50 is the average eligible player.

### 1.1 Official submission (Unstop entry)

**Top 10 batters:** 1. Suryakumar Yadav; 2. Dinesh Karthik; 3. David Miller; 4. Mark Chapman; 5. Towhid Hridoy; 6. Jos Buttler; 7. Tristan Stubbs; 8. Rohit Sharma; 9. Shubman Gill; 10. Jaker Ali Anik

**Top 10 bowlers:** 1. Sufiyan Muqeem; 2. Sunil Narine; 3. Varun Chakravarthy; 4. Mitchell Santner; 5. Jamie Overton; 6. Umran Malik; 7. Abrar Ahmed; 8. Matheesha Pathirana; 9. Mustafizur Rahman; 10. Rashid Khan

### 1.2 Top 10 batters under pressure

| Rank | Player | Primary team | Pressure rating | HP SR | Baseline SR | Δ SR | HP balls faced | Consistency |
|---|---|---|---|---|---|---|---|---|
| 1 | Suryakumar Yadav | Mumbai Indians (India) | 70.7 | 181.0 | 163.5 | +17.5 | 447 | 76% |
| 2 | Dinesh Karthik | Royal Challengers Bengaluru (India) | 68.6 | 175.0 | 159.0 | +16.0 | 332 | 63% |
| 3 | David Miller | Gujarat Titans (South Africa) | 66.9 | 165.5 | 138.4 | +27.2 | 516 | 57% |
| 4 | Mark Chapman | New Zealand | 66.8 | 172.4 | 135.8 | +36.6 | 203 | 68% |
| 5 | Towhid Hridoy | Bangladesh A (Bangladesh) | 66.5 | 155.9 | 117.3 | +38.6 | 222 | 68% |
| 6 | Jos Buttler | Rajasthan Royals (England) | 64.2 | 187.7 | 153.5 | +34.1 | 154 | 64% |
| 7 | Tristan Stubbs | Delhi Capitals (South Africa) | 63.6 | 163.1 | 141.8 | +21.3 | 390 | 64% |
| 8 | Rohit Sharma | Mumbai Indians (India) | 62.9 | 184.5 | 141.3 | +43.3 | 97 | 68% |
| 9 | Shubman Gill | Gujarat Titans (India) | 62.0 | 177.9 | 147.6 | +30.3 | 163 | 61% |
| 10 | Jaker Ali Anik | Bangladesh | 62.0 | 155.1 | 108.7 | +46.4 | 236 | 64% |

Δ SR = high-pressure strike rate minus the batter's own baseline strike rate (positive = faster under pressure).

- **#1 Suryakumar Yadav** (Mumbai Indians (India)): rating 70.7 from 447 high-pressure balls, HP SR 181.0 vs baseline 163.5.
- **#2 Dinesh Karthik** (Royal Challengers Bengaluru (India)) and **#3 David Miller** (Gujarat Titans (South Africa)) follow on ratings of 68.6 and 66.9.
- Largest lift on the player's own baseline inside the Top 10: **Jaker Ali Anik** (+46.4 SR points, positive = better under pressure).
- Evidence depth: the Top 10 averages 276 high-pressure balls (minimum 97) and a consistency rate of 65%; 3 of the 10 built most of that sample in T20Is, the rest in the IPL.

### 1.3 Top 10 bowlers under pressure

| Rank | Player | Primary team | Pressure rating | HP Econ | Baseline Econ | Δ Econ | HP balls bowled | Consistency |
|---|---|---|---|---|---|---|---|---|
| 1 | Sufiyan Muqeem | Pakistan A (Pakistan) | 79.7 | 4.92 | 6.68 | -1.76 | 232 | 74% |
| 2 | Sunil Narine | Kolkata Knight Riders | 72.8 | 6.10 | 6.97 | -0.87 | 369 | 76% |
| 3 | Varun Chakravarthy | Kolkata Knight Riders (India) | 71.0 | 7.00 | 8.15 | -1.15 | 665 | 70% |
| 4 | Mitchell Santner | Chennai Super Kings (New Zealand) | 70.2 | 6.26 | 7.53 | -1.27 | 479 | 69% |
| 5 | Jamie Overton | Chennai Super Kings (England) | 69.4 | 5.93 | 9.43 | -3.50 | 174 | 67% |
| 6 | Umran Malik | Sunrisers Hyderabad (India) | 69.0 | 6.82 | 9.99 | -3.17 | 162 | 56% |
| 7 | Abrar Ahmed | Pakistan | 68.9 | 4.86 | 7.24 | -2.38 | 216 | 63% |
| 8 | Matheesha Pathirana | Chennai Super Kings (Sri Lanka) | 68.6 | 6.94 | 8.35 | -1.42 | 529 | 72% |
| 9 | Mustafizur Rahman | Delhi Capitals (Bangladesh) | 67.7 | 7.03 | 7.63 | -0.60 | 472 | 66% |
| 10 | Rashid Khan | Gujarat Titans (Afghanistan) | 67.6 | 7.04 | 7.46 | -0.42 | 869 | 67% |

Δ Econ = high-pressure economy minus the bowler's own baseline economy (negative = tighter than usual under pressure); the rating compares the bowler with peers bowling in the same format, phase and pressure band, so a bowler can have a positive Δ Econ and still rate highly because high-pressure overs are expensive for everyone.

- **#1 Sufiyan Muqeem** (Pakistan A (Pakistan)): rating 79.7 from 232 high-pressure balls, HP economy 4.92 vs baseline 6.68.
- **#2 Sunil Narine** (Kolkata Knight Riders) and **#3 Varun Chakravarthy** (Kolkata Knight Riders (India)) follow on ratings of 72.8 and 71.0.
- Largest lift on the player's own baseline inside the Top 10: **Jamie Overton** (+3.50 runs/over, positive = better under pressure).
- Evidence depth: the Top 10 averages 417 high-pressure balls (minimum 162) and a consistency rate of 68%; 5 of the 10 built most of that sample in T20Is, the rest in the IPL.

*Primary team = the franchise (IPL) and country (T20I) the player appears for most often in the competition squads provided.*

---

## 2. Pressure Index: mathematical formulation

### 2.1 Design principles

1. **State before the ball.** Every term uses only runs, wickets and balls *before* the delivery, so the outcome of a ball can never influence its own pressure score.
2. **One currency.** Balls left and wickets in hand are converted into runs through an empirical resource curve, so "50 needed off 24 with 3 wickets down" and "50 needed off 24 with 8 down" are scored differently and consistently.
3. **Bounded and interpretable.** Each term is a logistic or exponential transform in [0, 1] and the weights sum to 1 in each innings, so PI ∈ [0, 1].

Notation: *r* runs scored, *w* wickets lost, *B* balls left, *N* balls in the innings (120, or the revised-overs value), σ(x) = 1/(1+e^{−x}).

### 2.2 Resource curve

$$E_v(B,w)=\hat\rho\big(\lceil B/6\rceil,\;w\big)\cdot B\cdot vf$$

where ρ̂ is the observed runs-still-to-come per ball left for each (overs-left bucket, wickets-lost) cell of first innings, shrunk to the bucket mean with prior weight 40 and forced non-increasing in *w*; *vf* ∈ [0.85, 1.20] is a venue factor, the venue's shrunk mean first-innings total over the global mean.

### 2.3 Second innings (chase)

With *R* the runs needed (target − *r*), ρ = *R* / E_v(B, w), RRR and CRR the required and current run rates:

$$PI_{2}=0.35\,\sigma\!\big(3\ln\rho\big)+0.15\,\sigma\!\Big(\tfrac{RRR-CRR}{3}\Big)+0.20\Big(1-\tfrac{B}{N}\Big)^{1.5}+0.30\,\exp\!\Big(-\tfrac{(\ln\rho)^2}{2\cdot 0.5^2}\Big)$$

and PI₂ = 0 once the target is reached. The four terms are: **difficulty** of the ask against what the remaining resources can deliver; the **required-versus-current rate gap**; **stage leverage**, since each ball matters more as the innings ends; and **closeness**, which peaks when the chase is exactly on par (ρ = 1).

### 2.4 First innings (setting a total)

With *par*<sub>v</sub> the venue-adjusted mean first-innings total, *sd* its standard deviation, and w̄(over) the average wickets lost at that stage:

$$PI_{1}=0.40\,\sigma\!\Big(\tfrac{par_v-(r+E_v)}{0.5\,sd}\Big)+0.25\,\sigma\!\big(w-\bar w_{\text{over}}\big)+0.35\Big(1-\tfrac{B}{N}\Big)^{1.5}$$

The first term is the projected total's shortfall to venue par (resources versus par), the second is a **collapse term** measuring wickets lost relative to what is normal at that stage (it flags "three down in the powerplay" without hard-coding it), and the third is innings progression.

### 2.5 Pressure bands

**High** PI ≥ 0.65, **Medium** 0.45 ≤ PI < 0.65, **Low** PI < 0.45.

### 2.6 Domain defence

**No outcome leakage.** Because the state is measured before the ball (cumulative totals minus the current delivery), a six cannot raise the pressure of the ball on which it was hit, and a wicket cannot make its own delivery look "high leverage". Pressure and performance are therefore measured on independent information.

**Dead games and garbage time.** A boundary in an already-lost chase should not be credited as clutch. The closeness term shrinks PI as the chase moves away from par in *either* direction (at ρ = 3 it falls to 0.09 of its maximum), and the player-level score compares each ball with the league average for the same format, phase and band, which removes the generic inflation of scoring in the death overs. We state plainly that this **attenuates rather than eliminates** the effect: the difficulty term rises as the chase becomes hopeless and partly offsets the closeness discount, so some near-lost situations can still land in the High band (section 6).

### 2.7 Empirical check: the bands behave differently

| Pressure band | Deliveries | Share of deliveries | Mean PI | Runs/ball | Dot-ball % | Boundary % | Wicket % |
|---|---|---|---|---|---|---|---|
| Low | 76,465 | 38.0% | 0.31 | 1.40 | 38.5 | 19.6 | 4.73 |
| Medium | 76,962 | 38.3% | 0.56 | 1.29 | 41.0 | 17.4 | 5.01 |
| High | 47,534 | 23.7% | 0.72 | 1.31 | 38.7 | 16.3 | 7.15 |

The wicket rate per delivery moves from 4.73% in the Low band to 5.01% in Medium and 7.15% in High (1.5× the Low-band rate), the run rate per ball from 1.40 to 1.31, and the boundary share from 19.6% to 16.3%. The index therefore isolates deliveries that are measurably different in what they cost the batting side, using outcomes the index never saw.

---

## 3. Player execution, baselines and empirical-Bayes shrinkage

### 3.1 Metrics (under pressure and at baseline)

| | Batter | Bowler |
|---|---|---|
| Run metric | runs off the bat per ball faced (strike rate = ×100; wides excluded) | runs conceded per delivery (economy = ×6 per legal ball; byes and leg-byes excluded) |
| Boundary % | balls where the bat scored 4 or 6 | boundaries conceded per delivery |
| Dot-ball % | balls with no runs off the bat | legal balls with no runs charged to the bowler |
| Wicket metric | dismissals of the striker per ball (retirements excluded) | bowler-credited wickets per delivery (run-outs and retirements excluded) |

*Baseline* = the same player's deliveries outside the High band.

### 3.2 Peer-adjusted residuals

For every delivery the league mean outcome of the same **format × phase × (High / not-High)** cell is subtracted, giving a residual that is free of the fact that death overs and T20Is score differently. High-pressure performance is the **PI-weighted mean residual** on High-band balls (weights = PI, effective sample n_eff = (Σw)² / Σw²), and the change on the player's own level is

$$\Delta_i=\bar r_i^{\,HP}-\bar r_i^{\,base}.$$

### 3.3 Composite and final score

Each metric is shrunk (3.4), standardised across eligible players, signed so that "better" is positive, and combined with fixed metric weights (batters: runs 0.40, boundary 0.15, dot 0.20, dismissal 0.25; bowlers: runs 0.40, boundary 0.15, dot 0.20, wicket 0.25). The result is a composite for pressure level (HP vs peers) and one for Δ vs own baseline. **Consistency** is the share of pressure matches (at least 6 High balls) whose standardised composite residual is positive, shrunk toward the league rate with prior weight 8. The final score and rating are

$$\text{Final}=60%\,z(\text{HP vs peers})+25%\,z(\Delta\text{ vs own baseline})+15%\,z(\text{consistency}),\qquad \text{Rating}=50+10\cdot\text{Final}.$$

Level carries the most weight because the brief asks who *delivers* when it matters; Δ rewards players who rise relative to their own norm; consistency rewards repeatability across matches rather than one big game.

### 3.4 Empirical-Bayes shrinkage

A player's raw mean residual x_i is noisy when the sample is small. We use the normal–normal posterior mean

$$\hat\theta_i=\mu+\frac{\tau^2}{\tau^2+se_i^2}\,(x_i-\mu),\qquad se_i^2=\frac{\sigma^2}{n_{\text{eff},i}},\qquad \tau^2=\max\!\big(\mathrm{Var}_{\text{between}}-\overline{se^2},\;0.10\,\mathrm{Var}_{\text{between}},\;10^{-12}\big)$$

where Var_between is the variance of raw player means among eligible players and σ² the per-delivery residual variance.

**Why method of moments.** The signal variance τ² is identified directly from the data as "observed spread between players minus the spread we expect from sampling noise alone". It is closed-form, deterministic and reproducible (no optimiser, starting values or priors to defend), and it is stable with a few hundred players. The 10% floor stops τ² collapsing to zero in a noisy metric, which would flatten every player to the mean.

**What it does to small samples.** A player with few high-pressure balls has a large se_i², so the raw number is pulled hard toward the average; a player with a large sample keeps most of it.

**Batters** (runs-per-ball metric: σ² = 2.961, τ² = 1.69e-02, average signal kept across eligible players 51%)

| Effective high-pressure balls (n_eff) | Shrinkage factor τ²/(τ²+σ²/n) | Share of raw signal kept |
|---|---|---|
| 30 | 0.15 | 15% |
| 60 | 0.25 | 25% |
| 120 | 0.41 | 41% |
| 240 | 0.58 | 58% |
| 480 | 0.73 | 73% |

The ten batters with the best *raw, unshrunk* high-pressure runs residual (any sample size) had a median of **1** high-pressure balls, and **10 of 10** fail the eligibility floors. The final Top 10 has a median of **229** balls and 0 players in common with that raw list.


**Bowlers** (runs-per-ball metric: σ² = 2.916, τ² = 1.88e-02, average signal kept across eligible players 53%)

| Effective high-pressure balls (n_eff) | Shrinkage factor τ²/(τ²+σ²/n) | Share of raw signal kept |
|---|---|---|
| 30 | 0.16 | 16% |
| 60 | 0.28 | 28% |
| 120 | 0.44 | 44% |
| 240 | 0.61 | 61% |
| 480 | 0.76 | 76% |

The ten bowlers with the best *raw, unshrunk* high-pressure runs residual (any sample size) had a median of **4** high-pressure balls, and **10 of 10** fail the eligibility floors. The final Top 10 has a median of **420** balls and 0 players in common with that raw list.


Together with the eligibility floors (section 4) this is what prevents one-match wonders from reaching the Top 10.

---

## 4. Tournament context and fair comparisons

**IPL and T20I together.** The two competitions differ in scoring environment and opposition depth, so no player is ever compared with a raw league-wide average. League expectations are computed **within each format × phase × pressure-band cell** before any cross-evaluation (table below), and a player's residual is measured against peers in the same cell. Players are pooled into one ranking; the dashboard additionally reports the share of each player's sample from each competition.

| Format | Phase | Deliveries | High-band share | League runs/ball | League wicket % |
|---|---|---|---|---|---|
| T20 | Death | 21,819 | 49.2% | 1.56 | 7.77 |
| T20 | Middle | 43,376 | 24.7% | 1.32 | 4.48 |
| T20 | PP | 29,451 | 1.5% | 1.37 | 4.09 |
| T20I | Death | 23,136 | 53.0% | 1.45 | 8.42 |
| T20I | Middle | 48,887 | 26.4% | 1.25 | 4.97 |
| T20I | PP | 34,292 | 1.3% | 1.25 | 4.80 |

*Format codes as in `competitions.csv`: `T20I` = internationals, `T20` = the franchise league.*

**Eligibility.** A player is ranked only with at least **60 high-pressure balls**, **8 high-pressure matches** and **100 baseline balls** (so the baseline is itself reliable). This leaves 118 of 769 batters and 173 of 532 bowlers ranked.

**Other fairness choices.** Super overs are excluded; rain-affected innings use the revised overs and target; the venue factor adjusts expected runs for high- and low-scoring grounds; ratings are comparable between batters and bowlers only within role.

---

## 5. Deep-dive case studies

All figures in this section come from the same pipeline and are read from the ball-level file.

### 5.1 Batters

#### Suryakumar Yadav: sustained acceleration under pressure

**Suryakumar Yadav** (Mumbai Indians (India)) ranks **#1** of 118 eligible batters, rating **70.7**, from **447** high-pressure balls faced in 31 pressure matches.

Under High pressure the batter scores at a strike rate of **181.0** against a baseline of 163.5 (Δ +17.5), with boundary 27.5% (baseline 24.0%) and dot-ball 26.6% (baseline 33.3%). A dismissal arrives once every 22 high-pressure balls.

Strike rate by band is 169.0 Low / 157.3 Medium / 181.0 High, so the High-band performance exceeds the Low-band level but the progression is not strictly monotone.

19% of the high-pressure balls came in the death overs (16–20), 79% in the middle overs and 1% in the powerplay; death-over High-band strike rate is 183.9.

Consistency: the player produced a positive composite in 76% of pressure matches (shrunk; percentile 100 among eligible).

| Band | Balls faced | Strike rate | Boundary % | Dot % | Dismissals/100 |
|---|---|---|---|---|---|
| Low | 1,218 | 169.0 | 24.9 | 31.7 | 4.5 |
| Medium | 1,094 | 157.3 | 23.1 | 35.1 | 3.8 |
| High | 447 | 181.0 | 27.5 | 26.6 | 4.5 |

#### Dinesh Karthik: finishing leverage in the death overs

**Dinesh Karthik** (Royal Challengers Bengaluru (India)) ranks **#2** of 118 eligible batters, rating **68.6**, from **332** high-pressure balls faced in 31 pressure matches.

Under High pressure the batter scores at a strike rate of **175.0** against a baseline of 159.0 (Δ +16.0), with boundary 25.0% (baseline 24.1%) and dot-ball 28.3% (baseline 35.8%). A dismissal arrives once every 26 high-pressure balls.

Strike rate by band is 184.2 Low / 153.2 Medium / 175.0 High, so the High-band performance does not exceed the Low-band level but the progression is not strictly monotone.

62% of the high-pressure balls came in the death overs (16–20), 38% in the middle overs and 0% in the powerplay; death-over High-band strike rate is 202.9.

Finishing leverage is supported by a death-weighted sample.

Consistency: the player produced a positive composite in 63% of pressure matches (shrunk; percentile 70 among eligible).

| Band | Balls faced | Strike rate | Boundary % | Dot % | Dismissals/100 |
|---|---|---|---|---|---|
| Low | 57 | 184.2 | 29.8 | 36.8 | 7.0 |
| Medium | 250 | 153.2 | 22.8 | 35.6 | 6.8 |
| High | 332 | 175.0 | 25.0 | 28.3 | 3.9 |


### 5.2 Bowlers

#### Sunil Narine: economy choke under pressure

**Sunil Narine** (Kolkata Knight Riders) ranks **#2** of 173 eligible bowlers, rating **72.8**, from **369** high-pressure balls bowled in 33 pressure matches.

Under High pressure the bowler concedes **6.10 runs/over** against a baseline of 6.97 (Δ -0.87; negative is better), with dot balls 42.6% (baseline 36.6%) and boundaries conceded 9.3% (baseline 11.7%). Wickets in the sample: 25, one every 15 balls.

Economy by band is 7.73 Low / 6.11 Medium / 6.10 High, so the bowler tightens as pressure rises.

Wickets per 100 balls: 3.06 Low / 4.01 Medium / 6.87 High.

30% of the high-pressure balls were bowled in the death overs, 70% in the middle overs and 0% in the powerplay.

Consistency: the player produced a positive composite in 76% of pressure matches (shrunk; percentile 100 among eligible).

| Band | Balls bowled | Economy | Dot % | Boundary conceded % | Wickets/100 |
|---|---|---|---|---|---|
| Low | 620 | 7.73 | 34.2 | 14.2 | 3.1 |
| Medium | 548 | 6.11 | 39.4 | 8.9 | 4.0 |
| High | 364 | 6.10 | 42.6 | 9.3 | 6.9 |

#### Varun Chakravarthy: wicket threat under pressure

**Varun Chakravarthy** (Kolkata Knight Riders (India)) ranks **#3** of 173 eligible bowlers, rating **71.0**, from **665** high-pressure balls bowled in 55 pressure matches.

Under High pressure the bowler concedes **7.00 runs/over** against a baseline of 8.15 (Δ -1.15; negative is better), with dot balls 43.4% (baseline 37.4%) and boundaries conceded 13.3% (baseline 17.4%). Wickets in the sample: 54, one every 12 balls.

Economy by band is 8.39 Low / 7.91 Medium / 7.00 High, so the bowler tightens as pressure rises.

Wickets per 100 balls: 5.21 Low / 6.13 Medium / 8.26 High.

29% of the high-pressure balls were bowled in the death overs, 71% in the middle overs and 1% in the powerplay.

Consistency: the player produced a positive composite in 70% of pressure matches (shrunk; percentile 97 among eligible).

| Band | Balls bowled | Economy | Dot % | Boundary conceded % | Wickets/100 |
|---|---|---|---|---|---|
| Low | 730 | 8.39 | 35.9 | 17.7 | 5.2 |
| Medium | 751 | 7.91 | 38.9 | 17.2 | 6.1 |
| High | 654 | 7.00 | 43.4 | 13.3 | 8.3 |


---

## 6. Sensitivity, limitations and extensions

### 6.1 Stability to the High-pressure threshold

> _Threshold runs not supplied._ Re-run Step 2 with `--high-pi 0.60` and `--high-pi 0.70` into separate folders, then pass them with `--sens 0.60=<folder> --sens 0.70=<folder>` to fill this table.


### 6.2 Stability to the final-score weights

**Batters**

| Weights (HP / Δ / consistency) | Top-10 overlap with base | Spearman ρ (all eligible) |
|---|---|---|
| Base (0.60/0.25/0.15) | 10/10 | 1.000 |
| HP-heavy (0.75/0.15/0.10) | 9/10 | 0.992 |
| Balanced (0.50/0.30/0.20) | 9/10 | 0.996 |
| No consistency (0.70/0.30/0.00) | 8/10 | 0.991 |
| HP only (1.00/0/0) | 8/10 | 0.959 |

**Bowlers**

| Weights (HP / Δ / consistency) | Top-10 overlap with base | Spearman ρ (all eligible) |
|---|---|---|
| Base (0.60/0.25/0.15) | 10/10 | 1.000 |
| HP-heavy (0.75/0.15/0.10) | 10/10 | 0.998 |
| Balanced (0.50/0.30/0.20) | 10/10 | 0.999 |
| No consistency (0.70/0.30/0.00) | 10/10 | 0.996 |
| HP only (1.00/0/0) | 10/10 | 0.986 |


### 6.3 Limitations (stated up front)

- **Venue-only adjustment.** Venue enters PI and expected runs, but opposition strength and bowler or batter quality faced are not adjusted at the player level, which matters most when T20I opponents differ widely.
- **Fixed phase boundaries.** Powerplay, middle and death are overs 1–6, 7–15 and 16–20 even in shortened matches.
- **Hopeless chases.** Closeness attenuates but does not remove the pressure score of near-lost situations (section 2.6); a damper using a win-probability model would be cleaner.
- **Expert-set weights and thresholds.** PI weights, the 0.65 cut-off and the final-score weights are judgement calls; sections 6.1 and 6.2 test their influence.
- **In-sample curves.** The resource curve, venue factors and league cells are fitted on the same seasons being evaluated.
- **Attribution.** Dismissals are credited to the striker, and context such as pitch, dew, ball type or field settings is not in the data.
- **Sample sizes.** Even after shrinkage, ranks near the cut line are uncertain; adjacent ranks should not be over-interpreted.

### 6.4 Future extensions

Opposition- and bowler-quality-adjusted residuals; a learned win-probability model so PI becomes change-in-win-probability (leverage); hierarchical Bayesian partial pooling with credible intervals on ranks; bootstrap rank stability; and fielding and partnership contributions.

---

## Appendix: reproducibility and parameters

Pipeline: `ball_by_ball.csv` → `rr_step2_pressure_engine.py` (PI, residuals, shrinkage, ranking) → this report; interactive view in `app.py`. All parameters (fitted and chosen) are stored in `pressure_config.json` and listed below.

| Parameter | Value |
|---|---|
| High / Medium PI cut-offs | 0.65 / 0.45 |
| Chase weights (state, rate, late, close) | 0.35, 0.15, 0.20, 0.30 |
| First-innings weights (par, collapse, late) | 0.40, 0.25, 0.35 |
| k (state), rate scale, closeness σ, lateness exponent | 3.0, 3.0, 0.5, 1.5 |
| Mean / s.d. of first-innings totals (fitted) | 167.2 / 37.4 |
| Final-score weights (HP, Δ, consistency) | 0.60, 0.25, 0.15 |
| Eligibility floors (HP balls, HP matches, baseline balls) | 60, 8, 100 |
