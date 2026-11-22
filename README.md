# Portfolio Desk

Portfolio Desk is a focused stock portfolio manager for tracking positions, understanding portfolio performance, and exporting a clean CSV summary. It is designed as a calm, private-by-default workspace rather than a noisy market terminal.

## What it includes

- Local demo login page with email/password fields, password visibility toggle, demo access, session persistence, and sign-out.
- Add, edit, and delete stock positions using ticker symbol, company name, sector, share quantity, average buy price, and current market price.
- Per-holding invested capital, market value, gain/loss amount, gain/loss percentage, and daily move display.
- Portfolio-level total value, invested capital, total return, top-position concentration, and allocation donut chart.
- Holdings search and sector filtering.
- Recent transaction-style activity summary.
- CSV export with calculated portfolio metrics.
- Responsive layouts for desktop, tablet, and mobile.
- Sample positions on first launch so the dashboard is immediately useful.

## Demo access

This project currently uses a front-end demo login rather than a remote authentication service. Choose **Use demo access** on the login page, or enter any non-empty email address and password. The signed-in state is stored in `localStorage` under `portfolio-desk-auth`; no credentials are transmitted or saved to a server.

Portfolio positions are stored locally in the browser under `portfolio-desk-positions`. Clearing browser storage resets the app to the sample portfolio.

## Calculations

For each holding:

```text
invested capital = shares × average buy price
market value     = shares × current market price
gain/loss        = market value − invested capital
gain/loss %      = gain/loss ÷ invested capital × 100
```

Portfolio totals are calculated by summing the corresponding values across all holdings. Allocation percentages use each holding's market value divided by total portfolio market value.

The current-price field uses editable sample snapshots. The interface is ready for a future market-data integration without requiring the dashboard calculation model to change.

## CSV export

Use **Export CSV** or **Download summary** from the dashboard. The browser downloads a file named like:

```text
portfolio_summary_2026-11-22.csv
```

The export includes ticker, company, sector, shares, average buy price, current price, invested capital, market value, gain/loss, and gain/loss percentage.

## Local development

Requirements:

- Node.js 18+
- npm

Install dependencies and start the Vite development server:

```bash
npm install
npm run dev
```

The managed project runs the app on port `3000`. For a production build:

```bash
npm run build
```

The compiled static output is written to `dist/`.

## Project structure

```text
.
├── index.html                 App shell and metadata
├── src/
│   ├── main.ts                State, rendering, calculations, login, and CSV export
│   ├── styles.css             Dashboard, login, drawer, and responsive styles
│   └── vite-env.d.ts          Vite client declarations
├── public/
│   └── manus-routes.json      Managed route manifest
├── app.config.ts              Project branding metadata
├── package.json               Development scripts and dependencies
└── TODO.md                    Delivered feature checklist
```

## Notes

This is a browser-first portfolio tracker, not a brokerage connection or trading system. Prices are entered or refreshed as snapshots, and the app does not place trades or provide investment advice.
