# Modeling Market Dynamics as Stochastic Processes on Curved Manifolds
*Inspired by Jim Simons' concept of holonomy from "The Man Who Solved the Market" by Gregory Zuckerman*

---

## Background to my Inspiration
Growing up, I loved the idea of owning your job by day trading — starting from nothing and trying to build something real with just discipline and focus. I tried all kinds of strategies — EMA crossovers, VWAP signals, combining technical setups with strong earnings — but I still saw trades fail for reasons I couldn’t explain. Everything would point in the right direction, and the stock would still tank.

Reading about holonomy in *The Man Who Solved the Market* made something click: maybe the market doesn’t move in a straight line. Maybe it curves, and that curve is shaped by all kinds of forces we don’t directly see - technical, fundamental, macro, even psychological. Holonomy helped me put a math word to something I already felt — that trades can drift off course as they move through this complex space.

Now I want to model that. I’m building a framework that treats the market as a path through a curved space. I’ll simulate price paths under “curvature” and compare them to standard Brownian motion models. Basically: can I turn this gut feeling I’ve had for years into something testable?

---

## Research Question
What if the market doesn't move in straight lines? How can we test how outside factors we don't directly see are creating structure for the market? Would a simulation using a bent path create a more accurate way to simulate prices?

---

## Summary
Rather than trying to predict the exact price level of SPY, this project focuses on modeling the underlying price dynamics and structural behavior of the market. The goal was to replicate how prices move generally over time. Such as their volatility, drift, and curvature—under different modeling assumptions:

I created two models to try to simulate how SPY moved in 2023:

- **Flat Model:** regular Geometric Brownian Motion with constant drift and volitility
- **Curved Model:** changes the drift each day based on how strong the previous daily returns are (using a 30 day rolling Sharpe ratio)

By comparing simulated trajectories to actual SPY data, the emphasis is on understanding the shape and structure of market motion, not on short-term price prediction accuracy.

I compared both models to the real SPY prices to see which one tracked better (using a correlation coefficient)

---

## Key Results (Results may differ based on simulation)
| Model                | Correlation with SPY | Improvement |
|----------------------|----------------------|-------------|
| Flat GBM             | 0.8284               | —           |
| Curved GBM (α = 0.9) | 0.9250               | +11.67%     |
| Optimized Curved     | **0.9295**           | **+12.20%** |


---

## Visualizations
Flat model vs actual SPY
- ![Flat Model vs Actaul](flat_model_vs_actual.png)

Curved model vs actual SPY:
- ![Curved Model vs Actaul](curved_model_vs_actual.png)

---

## Theoretical Background
The project builds on stochastic process theory, treating price action as a function of both randomness and structured curvature
- The Flat Model follows Geometric Brownian Motion (GBM), where prices evolve with constant drift (μ) and volatility (σ).
- The Curved Model modifies the drift dynamically using a 30-day rolling Sharpe ratio, introducing path-dependence — meaning market “momentum” and “structure” influence future returns.

This approach reflects the idea that markets move through curved spaces, where accumulated effects of past returns bend future trajectories. This is conceptually similar to holonomy in differential geometry, which is discuessed in the book "The Man Who Solved the Market", and is how I got the idea to do this project in the first place.

---

## Conclusion and Next Steps
This project demonstrates that even a simple adjustment to drift — allowing it to evolve with recent performance — can produce market simulations that more closely resemble real-world dynamics. While the goal was never to predict exact prices, the improved correlation of the curved model suggests that markets do exhibit structural tendencies that a flat Brownian framework can’t fully capture.

The next step is to extend this framework by introducing stochastic volatility, allowing both drift and volatility to evolve together. This would make the model more realistic and open the door to testing how market “curvature” behaves under different macro or volatility regimes.


## Author
Edward Peter Schwasnick
Statistics + CS Minor | University of Vermont
Quantitative and Strategic Thinking
