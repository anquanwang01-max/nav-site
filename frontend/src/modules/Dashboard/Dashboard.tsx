import React from 'react';

export const Dashboard: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', padding: '2rem', background: '#0f172a', minHeight: '100vh', color: 'white' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Quant Crypto Control Center</h1>
        <button style={{ padding: '0.5rem 1rem', borderRadius: '6px', background: '#38bdf8', border: 'none', color: '#0f172a' }}>
          Connect Wallet / API
        </button>
      </header>
      <section style={{ marginTop: '2rem', display: 'grid', gap: '1.5rem', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '1.5rem' }}>
          <h2>Realtime K-line</h2>
          <p>Hook up TradingView widget or custom charting here.</p>
        </div>
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '1.5rem' }}>
          <h2>Strategy Panel</h2>
          <ul>
            <li>Mean Reversion Alpha</li>
            <li>Momentum Scalper</li>
            <li>Arb Desk</li>
          </ul>
        </div>
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '1.5rem' }}>
          <h2>Risk Controls</h2>
          <p>Show account-level loss limits, leverage, and exposure.</p>
        </div>
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '1.5rem' }}>
          <h2>Orders</h2>
          <p>Place manual orders, view stops and take profits.</p>
        </div>
      </section>
    </div>
  );
};
