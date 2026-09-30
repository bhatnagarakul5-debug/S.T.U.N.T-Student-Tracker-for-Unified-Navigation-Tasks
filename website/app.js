/**
 * STUNT Official Showcase & Campus Ecosystem Logic (app.js)
 * Live dual-device sync simulator, interactive bunk calculator,
 * timetable preview, JARVIS AI terminal, and student registration.
 */

document.addEventListener('DOMContentLoaded', () => {
  initDualDeviceSimulator();
  initBunkCalculator();
  initTimetableSwitcher();
  initSplitterTool();
  initJarvisTerminal();
  initRegistrationModal();
  initDownloadHub();
});

// ==========================================================================
// 1. Dual Device Simulator (Phone -> Laptop Real-time Sync)
// ==========================================================================
function initDualDeviceSimulator() {
  const btnPhoneAtt = document.getElementById('btn-phone-att');
  const btnPhoneSplit = document.getElementById('btn-phone-split');
  
  const phoneAttPct = document.getElementById('phone-att-pct');
  const desktopAttPct = document.getElementById('desktop-att-pct');
  const desktopAttProgress = document.getElementById('desktop-att-progress');
  const desktopSyncToast = document.getElementById('desktop-sync-toast');
  const desktopTxnList = document.getElementById('desktop-txn-list');

  let attCount = 31;
  let totalClasses = 38;

  function triggerSyncAnimation(message) {
    if (!desktopSyncToast) return;
    desktopSyncToast.textContent = `⚡ Live Sync: ${message}`;
    desktopSyncToast.style.opacity = '1';
    desktopSyncToast.style.transform = 'translateY(0)';
    setTimeout(() => {
      desktopSyncToast.style.opacity = '0';
      desktopSyncToast.style.transform = 'translateY(-8px)';
    }, 3200);
  }

  if (btnPhoneAtt) {
    btnPhoneAtt.addEventListener('click', () => {
      attCount++;
      totalClasses++;
      const newPct = ((attCount / totalClasses) * 100).toFixed(1);
      
      // Update phone
      if (phoneAttPct) phoneAttPct.textContent = `${newPct}%`;
      
      // Update desktop
      if (desktopAttPct) desktopAttPct.textContent = `${newPct}% (${attCount}/${totalClasses})`;
      if (desktopAttProgress) desktopAttProgress.style.width = `${Math.min(100, newPct)}%`;
      
      btnPhoneAtt.textContent = '✓ Logged Present!';
      btnPhoneAtt.style.background = '#10b981';
      setTimeout(() => {
        btnPhoneAtt.textContent = '📱 Quick Tap: Mark Lecture Present';
        btnPhoneAtt.style.background = '';
      }, 1500);

      triggerSyncAnimation(`Attendance marked on Mobile (${newPct}%)`);
    });
  }

  if (btnPhoneSplit) {
    btnPhoneSplit.addEventListener('click', () => {
      const sampleBills = [
        { title: 'Cafeteria Lunch', amt: '₹480', per: '₹160/ea (3 ppl)' },
        { title: 'Hostel Wi-Fi Bill', amt: '₹900', per: '₹300/ea (3 ppl)' },
        { title: 'Printouts & Notes', amt: '₹120', per: '₹40/ea (3 ppl)' }
      ];
      const bill = sampleBills[Math.floor(Math.random() * sampleBills.length)];

      if (desktopTxnList) {
        const item = document.createElement('div');
        item.style.cssText = 'display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:12px; animation:fadeIn 0.3s ease;';
        item.innerHTML = `<span>🧾 ${bill.title}</span><span style="color:#f43f5e; font-weight:bold;">-${bill.amt} (${bill.per})</span>`;
        desktopTxnList.insertBefore(item, desktopTxnList.firstChild);
      }

      btnPhoneSplit.textContent = '✓ Bill Split & Notified!';
      btnPhoneSplit.style.background = '#06b6d4';
      setTimeout(() => {
        btnPhoneSplit.textContent = '🧾 Split ₹600 Lunch with 3 Friends';
        btnPhoneSplit.style.background = '';
      }, 1500);

      triggerSyncAnimation(`Split '${bill.title}' added to Desktop ledger`);
    });
  }
}

// ==========================================================================
// 2. Interactive Bunk Forecaster (Student Bunk Math Engine)
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

    // Enforce logic: attended cannot exceed total
    if (attended > total) {
      attended = total;
      sliderAtt.value = attended;
    }

    if (valAtt) valAtt.textContent = attended;
    if (valTot) valTot.textContent = total;
    if (valReq) valReq.textContent = `${(target * 100).toFixed(0)}%`;

    const currentPct = (attended / total) * 100;

    if (currentPct >= (target * 100)) {
      // Calculate how many more classes can be missed
      // (attended) / (total + x) >= target => attended >= target * total + target * x
      // target * x <= attended - target * total => x <= (attended / target) - total
      const maxBunks = Math.floor((attended / target) - total);
      resultPill.style.background = 'rgba(16, 185, 129, 0.15)';
      resultPill.style.color = '#34d399';
      resultPill.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      resultPill.innerHTML = `🎉 <b>${currentPct.toFixed(1)}% Attendance!</b> You can safely bunk <b>${Math.max(0, maxBunks)}</b> more lecture(s) without dropping below ${(target * 100).toFixed(0)}%!`;
    } else {
      // Calculate how many consecutive classes must be attended
      // (attended + y) / (total + y) >= target => attended + y >= target * total + target * y
      // y * (1 - target) >= target * total - attended
      const mustAttend = Math.ceil((target * total - attended) / (1 - target));
      resultPill.style.background = 'rgba(244, 63, 94, 0.15)';
      resultPill.style.color = '#fb7185';
      resultPill.style.borderColor = 'rgba(244, 63, 94, 0.4)';
      resultPill.innerHTML = `⚠️ <b>${currentPct.toFixed(1)}% Attendance Alert!</b> You MUST attend the next <b>${Math.max(1, mustAttend)}</b> consecutive lecture(s) to restore ${(target * 100).toFixed(0)}% eligibility!`;
    }
  }

  [sliderAtt, sliderTot, sliderReq].forEach(el => {
    if (el) el.addEventListener('input', calculateBunk);
  });

  calculateBunk();
}

// ==========================================================================
// 3. Dynamic Timetable Day Switcher
// ==========================================================================
function initTimetableSwitcher() {
  const tabs = document.querySelectorAll('.tt-day-tab');
  const container = document.getElementById('tt-schedule-container');

  const schedules = {
    Mon: [
      { time: '09:00 AM - 10:15 AM', sub: 'International Finance', room: 'Lecture Hall 204', faculty: 'Dr. Sharma' },
      { time: '10:30 AM - 11:45 AM', sub: 'Business Economics', room: 'Room 312', faculty: 'Prof. Roy' },
      { time: '01:00 PM - 02:30 PM', sub: 'Data Analytics Lab', room: 'CS Lab 2', faculty: 'Prof. Verma' }
    ],
    Tue: [
      { time: '09:30 AM - 11:00 AM', sub: 'Corporate Strategy', room: 'Hall B', faculty: 'Dr. Nair' },
      { time: '11:15 AM - 12:45 PM', sub: 'International Business', room: 'Room 105', faculty: 'Prof. Kapoor' }
    ],
    Wed: [
      { time: '09:00 AM - 10:15 AM', sub: 'International Finance', room: 'Lecture Hall 204', faculty: 'Dr. Sharma' },
      { time: '11:00 AM - 12:30 PM', sub: 'Financial Modeling', room: 'Lab 4', faculty: 'Dr. Sengupta' },
      { time: '02:00 PM - 03:15 PM', sub: 'Business Law', room: 'Room 201', faculty: 'Adv. Mehra' }
    ],
    Thu: [
      { time: '10:00 AM - 11:30 AM', sub: 'Marketing & Brand Strategy', room: 'Hall 3', faculty: 'Prof. Rao' },
      { time: '01:30 PM - 03:00 PM', sub: 'Business Economics', room: 'Room 312', faculty: 'Prof. Roy' }
    ],
    Fri: [
      { time: '09:00 AM - 10:30 AM', sub: 'International Business Seminar', room: 'Auditorium', faculty: 'Guest Speaker' },
      { time: '11:00 AM - 01:00 PM', sub: 'Capstone Project Review', room: 'Conference Room 1', faculty: 'Faculty Panel' }
    ]
  };

  function renderDay(day) {
    if (!container) return;
    const slots = schedules[day] || [];
    container.innerHTML = slots.map(s => `
      <div class="tt-slot-item">
        <div>
          <div style="font-weight: 700; font-size: 13px; color: #ffffff;">${s.sub}</div>
          <div style="font-size: 11px; color: #94a3b8;">📍 ${s.room} • 👤 ${s.faculty}</div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 11px; color: #38bdf8; background: rgba(6,182,212,0.1); padding: 4px 8px; border-radius: 6px;">
          ${s.time}
        </div>
      </div>
    `).join('');
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderDay(tab.dataset.day);
    });
  });

  renderDay('Mon');
}

// ==========================================================================
// 4. Instant Roommate Expense Splitter
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
    outShare.textContent = `₹${Number(share).toLocaleString()}`;
  }

  if (inAmt && inPpl) {
    inAmt.addEventListener('input', updateShare);
    inPpl.addEventListener('input', updateShare);
    updateShare();
  }

  if (btnUpi) {
    btnUpi.addEventListener('click', () => {
      const amt = parseFloat(inAmt.value) || 600;
      const ppl = Math.max(1, parseInt(inPpl.value, 10) || 3);
      const share = (amt / ppl).toFixed(0);
      navigator.clipboard?.writeText(`Hey! Your share for the bill is ₹${share}. Please pay via UPI.`);
      btnUpi.textContent = '✓ Copied Payment Text!';
      btnUpi.style.background = '#10b981';
      setTimeout(() => {
        btnUpi.textContent = '💬 Copy WhatsApp / UPI Request';
        btnUpi.style.background = '';
      }, 1800);
    });
  }
}

// ==========================================================================
// 5. JARVIS AI Interactive Terminal
// ==========================================================================
function initJarvisTerminal() {
  const inputEl = document.getElementById('jarvis-input');
  const outputEl = document.getElementById('jarvis-output');
  const btnSend = document.getElementById('jarvis-send');
  const chipButtons = document.querySelectorAll('.jarvis-prompt-chip');

  const responses = {
    viva: "⚡ <b>JARVIS Predictive Viva Analysis:</b>\n1. Explain the difference between Spot vs. Forward Exchange Rates.\n2. How does Purchasing Power Parity (PPP) influence sovereign currency valuation?\n3. What are currency swaps and why do multinational corporations hedge with them?",
    dupont: "⚡ <b>JARVIS Academic Synthesis:</b>\n• <b>DuPont Formula:</b> ROE = Profit Margin × Asset Turnover × Financial Leverage.\n• <b>Key Insight:</b> It disaggregates return on equity to reveal whether profitability stems from high margins, efficient asset use, or debt financing.",
    bunk: "⚡ <b>JARVIS Bunk Algorithm:</b>\nBased on your current 82% attendance, you have a safe buffer of <b>3 classes</b> before hitting the 75% boundary. Recommendation: Keep 1 emergency buffer class for sick days!"
  };

  function typeResponse(text) {
    if (!outputEl) return;
    outputEl.innerHTML = '';
    let i = 0;
    const interval = setInterval(() => {
      outputEl.innerHTML = text.slice(0, i);
      i += 3;
      if (i > text.length) {
        outputEl.innerHTML = text;
        clearInterval(interval);
      }
    }, 15);
  }

  function handlePrompt(promptText) {
    const lower = promptText.toLowerCase();
    if (lower.includes('viva') || lower.includes('question')) {
      typeResponse(responses.viva);
    } else if (lower.includes('dupont') || lower.includes('finance')) {
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
      if (inputEl) inputEl.value = chip.dataset.prompt;
      handlePrompt(chip.dataset.prompt);
    });
  });
}

// ==========================================================================
// 6. Registration Modal & Digital Student ID Card Generator
// ==========================================================================
function initRegistrationModal() {
  const modal = document.getElementById('reg-modal');
  const openButtons = document.querySelectorAll('.open-reg-btn');
  const closeBtn = document.getElementById('reg-modal-close');
  const regForm = document.getElementById('reg-form');
  const cardPreviewWrap = document.getElementById('id-card-preview-wrap');

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (modal) modal.classList.add('active');
    });
  });

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('active');
    });
  }

  if (regForm) {
    regForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value || 'Akul';
      const college = document.getElementById('reg-college').value || 'University Campus';
      const course = document.getElementById('reg-course').value || 'B.Tech CSE';
      const batch = document.getElementById('reg-batch').value || '2026 - 2030';
      const sem = document.getElementById('reg-sem').value || 'Semester 3';

      const stuId = `STU-2026-${Math.floor(1000 + Math.random() * 9000)}`;

      if (cardPreviewWrap) {
        cardPreviewWrap.innerHTML = `
          <div class="id-card" style="animation:fadeIn 0.5s ease;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
              <span style="font-size:11px; font-weight:800; color:#a78bfa; letter-spacing:1.5px;">STUNT VERIFIED STUDENT PASS</span>
              <span style="font-size:10px; background:#10b981; color:#064e3b; padding:2px 8px; border-radius:999px; font-weight:bold;">ACTIVE</span>
            </div>
            <div style="display:flex; gap:16px; align-items:center; margin-bottom:14px;">
              <div style="width:52px; height:52px; border-radius:12px; background:linear-gradient(135deg, #8b5cf6, #06b6d4); display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:bold; color:#fff;">
                ${name.charAt(0)}
              </div>
              <div>
                <div style="font-size:18px; font-weight:800; color:#ffffff;">${name}</div>
                <div style="font-size:12px; color:#cbd5e1;">${course} • ${sem}</div>
                <div style="font-size:11px; color:#94a3b8;">${college} (${batch})</div>
              </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:flex-end; font-family:var(--font-mono); font-size:11px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
              <div>
                <div style="color:#64748b; font-size:9px;">STUDENT ID</div>
                <div style="color:#38bdf8; font-weight:bold;">${stuId}</div>
              </div>
              <div style="color:#10b981; font-weight:bold;">✓ CLOUD SYNC READY</div>
            </div>
          </div>
          <div style="text-align:center; margin-top:16px;">
            <span style="color:#34d399; font-weight:700; font-size:14px;">🎉 Account Created & Cloud Sync Reserved!</span>
          </div>
        `;
      }

      // Store in localStorage
      localStorage.setItem('stunt_registered_student', JSON.stringify({
        name, college, course, batch, sem, stuId
      }));
    });
  }
}

// ==========================================================================
// 7. Multi-Platform Download Hub & OS Detector
// ==========================================================================
function initDownloadHub() {
  const winBtn = document.getElementById('dl-win-tile');
  const macBtn = document.getElementById('dl-mac-tile');
  const andBtn = document.getElementById('dl-and-tile');

  // Detect user agent
  const ua = navigator.userAgent.toLowerCase();
  if (ua.includes('win') && winBtn) {
    winBtn.style.borderColor = '#8b5cf6';
    winBtn.style.boxShadow = '0 0 25px rgba(139, 92, 246, 0.4)';
    const badge = winBtn.querySelector('.dl-rec-badge');
    if (badge) badge.style.display = 'inline-block';
  } else if (ua.includes('mac') && macBtn) {
    macBtn.style.borderColor = '#06b6d4';
    macBtn.style.boxShadow = '0 0 25px rgba(6, 182, 212, 0.4)';
  } else if (ua.includes('android') && andBtn) {
    andBtn.style.borderColor = '#10b981';
    andBtn.style.boxShadow = '0 0 25px rgba(16, 185, 129, 0.4)';
  }
}
