/**
 * STUNT — Official Showcase & Sovereign Campus OS (app.js)
 * Clean, lightweight, client-side interactions.
 * Developed by Akul Bhatnagar (NMIMS Mumbai BBA IB).
 */

document.addEventListener('DOMContentLoaded', () => {
  initBunkCalculator();
  initTimetableSwitcher();
  initSplitterTool();
  initJarvisTerminal();
  initPrivacyModal();
  initRegistrationModal();
});

// ==========================================================================
// 1. Interactive 75% Attendance & Bunk Forecaster (Integer Precision)
// ==========================================================================
function initBunkCalculator() {
  const sliderAtt = document.getElementById('bunk-slider-att');
  const sliderTot = document.getElementById('bunk-slider-tot');
  const sliderReq = document.getElementById('bunk-slider-req');

  const valAtt = document.getElementById('bunk-val-att');
  const valTot = document.getElementById('bunk-val-tot');
  const valReq = document.getElementById('bunk-val-req');
  const resultPill = document.getElementById('bunk-result-pill');

  function calculateBunk() {
    if (!sliderAtt || !sliderTot || !sliderReq || !resultPill) return;

    let attended = parseInt(sliderAtt.value, 10);
    let total = parseInt(sliderTot.value, 10);
    const target = parseInt(sliderReq.value, 10) / 100.0;

    // Constrain: attended cannot exceed total
    if (attended > total) {
      attended = total;
      sliderAtt.value = attended;
    }

    if (valAtt) valAtt.textContent = attended;
    if (valTot) valTot.textContent = total;
    if (valReq) valReq.textContent = `${(target * 100).toFixed(0)}%`;

    const currentPct = (attended / total) * 100;

    if (currentPct >= target * 100) {
      // (attended) / (total + x) >= target => x <= (attended / target) - total
      const maxBunks = Math.floor(attended / target - total);
      resultPill.className = 'status-badge safe';
      resultPill.innerHTML = `✓ <b>${currentPct.toFixed(1)}% Attendance</b> — You can safely bunk <b>${Math.max(0, maxBunks)}</b> lecture(s) before dropping below ${(target * 100).toFixed(0)}%.`;
    } else {
      // (attended + y) / (total + y) >= target => y >= (target * total - attended) / (1 - target)
      const mustAttend = Math.ceil((target * total - attended) / (1 - target));
      resultPill.className = 'status-badge alert';
      resultPill.innerHTML = `⚠️ <b>${currentPct.toFixed(1)}% Attendance Alert</b> — You must attend the next <b>${Math.max(1, mustAttend)}</b> consecutive lecture(s) to restore ${(target * 100).toFixed(0)}% eligibility.`;
    }
  }

  [sliderAtt, sliderTot, sliderReq].forEach(el => {
    if (el) el.addEventListener('input', calculateBunk);
  });

  calculateBunk();
}

// ==========================================================================
// 2. Dynamic Timetable Matrix
// ==========================================================================
function initTimetableSwitcher() {
  const tabs = document.querySelectorAll('.tt-tab, .tt-day-tab');
  const container = document.getElementById('tt-schedule-container');

  const schedules = {
    Mon: [
      { time: '09:00 - 10:15 AM', sub: 'International Finance', room: 'Hall 204', faculty: 'Dr. Sharma' },
      { time: '10:30 - 11:45 AM', sub: 'Business Economics', room: 'Room 312', faculty: 'Prof. Roy' },
      { time: '01:00 - 02:30 PM', sub: 'Data Analytics & Modeling', room: 'CS Lab 2', faculty: 'Prof. Verma' }
    ],
    Tue: [
      { time: '09:30 - 11:00 AM', sub: 'Corporate Strategy & Governance', room: 'Hall B', faculty: 'Dr. Nair' },
      { time: '11:15 - 12:45 PM', sub: 'Global Trade Logistics', room: 'Room 105', faculty: 'Prof. Kapoor' }
    ],
    Wed: [
      { time: '09:00 - 10:15 AM', sub: 'International Finance', room: 'Hall 204', faculty: 'Dr. Sharma' },
      { time: '11:00 - 12:30 PM', sub: 'Financial Modeling & Valuation', room: 'Lab 4', faculty: 'Dr. Sengupta' },
      { time: '02:00 - 03:15 PM', sub: 'Business Law & Ethics', room: 'Room 201', faculty: 'Adv. Mehra' }
    ],
    Thu: [
      { time: '10:00 - 11:30 AM', sub: 'Marketing & Brand Strategy', room: 'Hall 3', faculty: 'Prof. Rao' },
      { time: '01:30 - 03:00 PM', sub: 'Business Economics', room: 'Room 312', faculty: 'Prof. Roy' }
    ],
    Fri: [
      { time: '09:00 - 10:30 AM', sub: 'International Business Seminar', room: 'Auditorium', faculty: 'Visiting Fellow' },
      { time: '11:00 - 01:00 PM', sub: 'Capstone Project Evaluation', room: 'Boardroom 1', faculty: 'Faculty Panel' }
    ]
  };

  function renderDay(day) {
    if (!container) return;
    const slots = schedules[day] || [];
    container.innerHTML = slots.map(s => `
      <div class="tt-row">
        <div>
          <div style="font-weight: 600; color: #ffffff;">${s.sub}</div>
          <div style="font-size: 11px; color: var(--text-tertiary);">📍 ${s.room} • 👤 ${s.faculty}</div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 11px; color: #a1a1aa; background: #1c1c22; padding: 4px 8px; border-radius: 4px; border: 1px solid var(--border);">
          ${s.time}
        </div>
      </div>
    `).join('');
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderDay(tab.dataset.day || tab.textContent.trim());
    });
  });

  renderDay('Mon');
}

// ==========================================================================
// 3. Hostel / Roommate Bill Splitter
// ==========================================================================
function initSplitterTool() {
  const inAmt = document.getElementById('split-input-amt');
  const inPpl = document.getElementById('split-input-ppl');
  const outShare = document.getElementById('split-output-share');
  const btnUpi = document.getElementById('split-btn-upi');

  function updateShare() {
    if (!inAmt || !inPpl || !outShare) return;
    const amt = parseFloat(inAmt.value) || 0;
    const ppl = Math.max(1, parseInt(inPpl.value, 10) || 1);
    const share = (amt / ppl).toFixed(0);
    outShare.textContent = `₹${Number(share).toLocaleString('en-IN')}`;
  }

  if (inAmt && inPpl) {
    inAmt.addEventListener('input', updateShare);
    inPpl.addEventListener('input', updateShare);
    updateShare();
  }

  if (btnUpi) {
    btnUpi.addEventListener('click', () => {
      const amt = parseFloat(inAmt?.value) || 1200;
      const ppl = Math.max(1, parseInt(inPpl?.value, 10) || 4);
      const share = (amt / ppl).toFixed(0);
      const text = `Hey! Your share for the shared expenses is ₹${share}. Please pay via UPI. (Calculated via STUNT)`;
      
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text);
      }
      const prevText = btnUpi.textContent;
      btnUpi.textContent = '✓ Copied Payment Text to Clipboard!';
      setTimeout(() => {
        btnUpi.textContent = prevText;
      }, 2000);
    });
  }
}

// ==========================================================================
// 4. J.A.R.V.I.S. Mark 58 Terminal Integration
// ==========================================================================
function initJarvisTerminal() {
  const inputEl = document.getElementById('jarvis-input');
  const outputEl = document.getElementById('jarvis-output');
  const btnSend = document.getElementById('jarvis-send');
  const chipButtons = document.querySelectorAll('.chip-btn, .jarvis-prompt-chip');

  const responses = {
    viva: "⚡ [JARVIS Mark 58 // stunt_bridge.py]\n\nPredictive Viva Questions (International Finance):\n1. Distinguish between Covered Interest Arbitrage (CIA) and Uncovered Interest Parity (UIP).\n2. How does Purchasing Power Parity (PPP) forecast long-term sovereign currency exchange rates?\n3. Explain the mechanics of currency swaps in mitigating multinational foreign exchange exposure.",
    dupont: "⚡ [JARVIS Mark 58 // stunt_bridge.py]\n\nDuPont Analysis Breakdown:\n• Formula: ROE = Net Profit Margin × Total Asset Turnover × Financial Leverage Multiplier.\n• Academic Insight: Pinpoints whether a company's high ROE is driven by operational pricing power (margin), capital efficiency (turnover), or risky balance sheet gearing (leverage).",
    bunk: "⚡ [JARVIS Mark 58 // stunt_bridge.py]\n\nAttendance Safety Engine:\n• Current Status: 32 / 38 classes attended (84.2%). Target: 75%.\n• Buffer: You have 4 allowable absences remaining.\n• Verdict: Safe to attend group project prep tomorrow. 1 emergency buffer class recommended for exam week."
  };

  function typeResponse(text) {
    if (!outputEl) return;
    outputEl.innerHTML = '';
    let i = 0;
    const interval = setInterval(() => {
      outputEl.innerHTML = text.slice(0, i).replace(/\n/g, '<br>');
      i += 4;
      if (i > text.length) {
        outputEl.innerHTML = text.replace(/\n/g, '<br>');
        clearInterval(interval);
      }
    }, 12);
  }

  function handlePrompt(promptText) {
    const lower = promptText.toLowerCase();
    if (lower.includes('viva') || lower.includes('question') || lower.includes('finance')) {
      typeResponse(responses.viva);
    } else if (lower.includes('dupont') || lower.includes('roe') || lower.includes('margin')) {
      typeResponse(responses.dupont);
    } else {
      typeResponse(responses.bunk);
    }
  }

  if (btnSend && inputEl) {
    btnSend.addEventListener('click', () => {
      if (inputEl.value.trim()) {
        handlePrompt(inputEl.value);
      }
    });
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && inputEl.value.trim()) {
        handlePrompt(inputEl.value);
      }
    });
  }

  chipButtons.forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.dataset.prompt || chip.textContent.trim();
      if (inputEl) inputEl.value = prompt;
      handlePrompt(prompt);
    });
  });
}

// ==========================================================================
// 5. Data Sovereignty & Privacy Policy Modal
// ==========================================================================
function initPrivacyModal() {
  const modal = document.getElementById('privacy-modal');
  const openButtons = document.querySelectorAll('.open-privacy-modal-btn');
  const closeBtn = document.getElementById('privacy-modal-close');
  const dismissBtn = document.getElementById('privacy-modal-dismiss');

  function openModal() {
    if (modal) modal.classList.add('active');
  }

  function closeModal() {
    if (modal) modal.classList.remove('active');
  }

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openModal();
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (dismissBtn) dismissBtn.addEventListener('click', closeModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

// ==========================================================================
// 6. Student Onboarding Modal & Verified Digital Pass
// ==========================================================================
function initRegistrationModal() {
  const modal = document.getElementById('reg-modal');
  const openButtons = document.querySelectorAll('.open-reg-btn');
  const closeBtn = document.getElementById('reg-modal-close');
  const regForm = document.getElementById('reg-form');
  const cardPreviewWrap = document.getElementById('id-card-preview-wrap');

  function openModal() {
    if (modal) modal.classList.add('active');
  }

  function closeModal() {
    if (modal) modal.classList.remove('active');
  }

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openModal();
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeModal();
    }
  });

  if (regForm) {
    regForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name')?.value || 'Student User';
      const college = document.getElementById('reg-college')?.value || 'NMIMS Mumbai';
      const course = document.getElementById('reg-course')?.value || 'BBA International Business';
      const sem = document.getElementById('reg-sem')?.value || 'Semester 3';
      const contact = document.getElementById('reg-contact')?.value || 'local@stunt.internal';

      const stuId = `STU-2026-${Math.floor(1000 + Math.random() * 9000)}`;

      if (cardPreviewWrap) {
        cardPreviewWrap.innerHTML = `
          <div style="background: #111116; border: 1px solid var(--border); border-radius: 8px; padding: 18px; margin-bottom: 20px; font-family: var(--font-sans);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px;">
              <span style="font-size: 10px; font-weight: 700; color: #a1a1aa; letter-spacing: 0.1em;">STUNT VERIFIED STUDENT PROFILE</span>
              <span style="font-size: 10px; background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 2px 8px; border-radius: 999px; font-weight: 600;">LOCAL SOVEREIGN</span>
            </div>
            <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 12px;">
              <div style="width: 44px; height: 44px; border-radius: 8px; background: #27272a; border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; color: #ffffff;">
                ${name.charAt(0).toUpperCase()}
              </div>
              <div>
                <div style="font-size: 15px; font-weight: 700; color: #ffffff;">${name}</div>
                <div style="font-size: 12px; color: var(--text-secondary);">${course} • ${sem}</div>
                <div style="font-size: 11px; color: var(--text-tertiary);">${college}</div>
              </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end; font-family: var(--font-mono); font-size: 11px; padding-top: 8px; border-top: 1px solid var(--border-subtle);">
              <div>
                <div style="color: var(--text-tertiary); font-size: 9px;">STUDENT ID</div>
                <div style="color: #ffffff; font-weight: 600;">${stuId}</div>
              </div>
              <div style="color: #34d399; font-weight: 500;">✓ LOCAL STORAGE READY</div>
            </div>
          </div>
        `;
      }

      localStorage.setItem('stunt_profile', JSON.stringify({
        name, college, course, sem, contact, stuId, registeredAt: new Date().toISOString()
      }));
    });
  }
}
