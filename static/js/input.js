// Pretty number formatter
const fmt = n => Number(n).toLocaleString(undefined);

// Hook up “Samples” live output
const samples = document.getElementById('n_samples');
const samplesOut = document.getElementById('samples_out');
samples.addEventListener('input', () => samplesOut.textContent = fmt(samples.value));
samplesOut.textContent = fmt(samples.value);

const $ = id => document.getElementById(id);
const ids = [
  'spec_bsw','spec_salt','n_samples','flow_min','flow_max',
  'T_min','T_max','V_min','V_max',
  'ppm_min','ppm_max','wash_min','wash_max','use_minimize_wash',
  'baseline_flow','baseline_demulsifier','baseline_temp','baseline_voltage','baseline_wash'
];

// Defaults (used by Reset)
const defaults = {
  spec_bsw: 0.5, spec_salt: 5.0, n_samples: 3000, flow_min: 20000, flow_max: 60000,
  T_min: 105, T_max: 130, V_min: 22, V_max: 32,
  ppm_min: 10, ppm_max: 90, wash_min: 0.5, wash_max: 4.0,
  use_minimize_wash: false,
  baseline_flow: 30000, baseline_demulsifier: 70, baseline_temp: 120,
  baseline_voltage: 28, baseline_wash: 2.0
};

// Restore from localStorage if present
(function restore(){
  const saved = localStorage.getItem('desalterInputs');
  if(!saved) return;
  try {
    const obj = JSON.parse(saved);
    ids.forEach(k => {
      if ($(k).type === 'checkbox') { $(k).checked = !!obj[k]; }
      else $(k).value = obj[k];
    });
    samplesOut.textContent = fmt($('n_samples').value);
  } catch {}
})();

// Validation helpers
function rangeOK(min, max){ return Number(min) < Number(max); }

function showError(msg){
  const e = $('error-message');
  if (e) {
    e.textContent = msg;
    e.style.display = 'block';
    e.classList.add('show');
    setTimeout(() => e.classList.remove('show'), 5000);
  }
  const ok = $('success-message');
  if (ok) {
    ok.style.display = 'none';
    ok.classList.remove('show');
  }
}

function showOK(msg){
  const o = $('success-message');
  if (o) {
    o.textContent = msg;
    o.style.display = 'block';
    o.classList.add('show');
    setTimeout(() => o.classList.remove('show'), 3000);
  }
  const err = $('error-message');
  if (err) {
    err.style.display = 'none';
    err.classList.remove('show');
  }
}

function collect(){
  const obj = {};
  ids.forEach(k => obj[k] = ($(`${k}`).type === 'checkbox') ? $(`${k}`).checked : Number($(`${k}`).value));
  return obj;
}

function validate(p){
  if (!rangeOK(p.flow_min, p.flow_max)) return 'Flow min must be less than max.';
  if (!rangeOK(p.T_min, p.T_max)) return 'Temperature min must be less than max.';
  if (!rangeOK(p.V_min, p.V_max)) return 'Voltage min must be less than max.';
  if (!rangeOK(p.ppm_min, p.ppm_max)) return 'Demulsifier min must be less than max.';
  if (!rangeOK(p.wash_min, p.wash_max)) return 'Wash water min must be less than max.';
  if (p.spec_bsw < 0.05 || p.spec_bsw > 2.0) return 'Target BS&W must be between 0.05 and 2.0%.';

  // Baseline validation
  if (p.baseline_flow < 1000 || p.baseline_flow > 100000) return 'Baseline flow must be between 1,000 and 100,000 BPD.';
  if (p.baseline_demulsifier < 1 || p.baseline_demulsifier > 200) return 'Baseline demulsifier must be between 1 and 200 ppm.';
  if (p.baseline_temp < 50 || p.baseline_temp > 200) return 'Baseline temperature must be between 50 and 200°C.';
  if (p.baseline_voltage < 10 || p.baseline_voltage > 50) return 'Baseline voltage must be between 10 and 50 kV.';
  if (p.baseline_wash < 0.1 || p.baseline_wash > 10) return 'Baseline wash must be between 0.1 and 10%.';

  return '';
}

$('resetBtn').addEventListener('click', () => {
  Object.entries(defaults).forEach(([k,v]) => {
    if ($(k).type === 'checkbox') $(k).checked = !!v; else $(k).value = v;
  });
  samplesOut.textContent = fmt(defaults.n_samples);
  localStorage.removeItem('desalterInputs');
  showOK('Defaults restored.');
});

$('startBtn').addEventListener('click', async () => {
  const params = collect();
  const err = validate(params);
  if (err){ showError(err); return; }

  // Show loading overlay
  showLoadingOverlay();

  // Persist for later pages
  localStorage.setItem('desalterInputs', JSON.stringify(params));

  // Simulate processing time with multiple stages
  setTimeout(() => {
    updateProgressStep(1);
  }, 1000);

  setTimeout(() => {
    updateProgressStep(2);
  }, 2500);

  setTimeout(() => {
    updateProgressStep(3);
  }, 4000);

  setTimeout(() => {
    updateProgressStep(4);
    // Show result page after final step
    setTimeout(() => {
      showResultsPage();
    }, 1500);
  }, 5500);
});

// Loading overlay functions
function showLoadingOverlay() {
  const overlay = $('loadingOverlay');
  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function hideLoadingOverlay() {
  const overlay = $('loadingOverlay');
  overlay.classList.remove('active');
  document.body.style.overflow = '';
}

function updateProgressStep(stepNumber) {
  const steps = document.querySelectorAll('.progress-step');
  steps.forEach((step, index) => {
    if (index < stepNumber) {
      step.style.opacity = '1';
      step.style.transform = 'translateY(0)';
    }
  });

  // Update progress text based on current step
  const titles = [
    'Optimizing Process',
    'Validating Parameters',
    'Running Algorithm',
    'Generating Results',
    'Complete!'
  ];

  const subtitles = [
    'Analyzing parameters and calculating optimal settings...',
    'Checking parameter ranges and constraints...',
    'Applying advanced mathematical models...',
    'Finding the best parameter combination...',
    'Optimization complete! Preparing results...'
  ];

  const titleElement = document.querySelector('.progress-title');
  const subtitleElement = document.querySelector('.progress-subtitle');

  if (titleElement && subtitleElement) {
    titleElement.textContent = titles[stepNumber] || titles[0];
    subtitleElement.textContent = subtitles[stepNumber] || subtitles[0];
  }
}

function showResultsPage() {
  // Hide the overlay and show success message
  hideLoadingOverlay();
  showOK('Optimization complete! Results ready.');

  // Navigate to the results page after a brief delay
  setTimeout(() => {
    window.location.href = '/results';
  }, 1000);
}

// Soft Glass Mount Animation System
document.addEventListener('DOMContentLoaded', () => {
  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReducedMotion) {
    // Initialize IntersectionObserver for glass mount sections
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;

          // Add reveal class to glass mount elements
          if (element.classList.contains('glass-mount')) {
            element.classList.add('reveal');

            // Trigger staggered children animation
            const staggerItems = element.querySelectorAll('.stagger-item');
            staggerItems.forEach((item, index) => {
              setTimeout(() => {
                item.classList.add('reveal');
              }, index * 80); // 80ms stagger delay
            });
          }

          // Stop observing after animation is triggered
          observer.unobserve(element);
        }
      });
    }, observerOptions);

    // Observe all glass mount elements
    const glassMountElements = document.querySelectorAll('.glass-mount');
    glassMountElements.forEach(element => {
      observer.observe(element);
    });

    // Auto-trigger animations for elements already in viewport
    const autoTriggerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal');
          autoTriggerObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px' });

    // Auto-trigger stagger items that are immediately visible
    setTimeout(() => {
      const visibleStaggerItems = document.querySelectorAll('.stagger-item:not(.reveal)');
      visibleStaggerItems.forEach(item => {
        autoTriggerObserver.observe(item);
      });
    }, 100);
  } else {
    // Respect reduced motion preference - just show elements without animation
    const allAnimatedElements = document.querySelectorAll('.glass-mount, .stagger-item');
    allAnimatedElements.forEach(element => {
      element.classList.add('reveal');
    });
  }
});
