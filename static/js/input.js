// Pretty number formatter
const fmt = n => Number(n).toLocaleString(undefined);

// Hook up "Samples" live output
const samples = document.getElementById('n_samples');
const samplesOut = document.getElementById('samples_out');

if (samples && samplesOut) {
samples.addEventListener('input', () => samplesOut.textContent = fmt(samples.value));
samplesOut.textContent = fmt(samples.value);
}

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
      const el = $(k);
      if (el) {
        if (el.type === 'checkbox') { el.checked = !!obj[k]; }
        else el.value = obj[k];
      }
    });
    const nSamplesEl = $('n_samples');
    if (nSamplesEl) {
      samplesOut.textContent = fmt(nSamplesEl.value);
    }
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
  ids.forEach(k => {
    const el = $(`${k}`);
    if (el) {
      obj[k] = (el.type === 'checkbox') ? el.checked : Number(el.value);
    }
  });
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
    const el = $(k);
    if (el) {
      if (el.type === 'checkbox') el.checked = !!v; else el.value = v;
    }
  });
  if (samplesOut) {
    samplesOut.textContent = fmt(defaults.n_samples);
  }
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
    window.location.href = './result.html';
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

  // Initialize drag and drop for priority items
  initializePriorityDragDrop();
});

// Priority Drag and Drop System
function initializePriorityDragDrop() {
  const priorityGrid = document.getElementById('priorityGrid');
  if (!priorityGrid) return;

  const priorityItems = priorityGrid.querySelectorAll('.priority-item[draggable="true"]');
  let draggedElement = null;
  let touchStartY = 0;
  let touchStartX = 0;

  priorityItems.forEach(item => {
    // Desktop drag events
    item.addEventListener('dragstart', handleDragStart);
    item.addEventListener('dragover', handleDragOver);
    item.addEventListener('drop', handleDrop);
    item.addEventListener('dragend', handleDragEnd);
    item.addEventListener('dragenter', handleDragEnter);
    item.addEventListener('dragleave', handleDragLeave);

    // Touch events for mobile
    item.addEventListener('touchstart', handleTouchStart, { passive: false });
    item.addEventListener('touchmove', handleTouchMove, { passive: false });
    item.addEventListener('touchend', handleTouchEnd, { passive: false });
  });

  function handleDragStart(e) {
    console.log('Drag start initiated on:', this);
    draggedElement = this;
    console.log('Set draggedElement to:', draggedElement);
    this.classList.add('dragging');

    // Create professional drag image
    const dragImage = this.cloneNode(true);
    dragImage.style.position = 'absolute';
    dragImage.style.top = '-1000px';
    dragImage.style.opacity = '0.8';
    dragImage.style.transform = 'rotate(3deg) scale(1.05)';
    dragImage.style.pointerEvents = 'none';
    document.body.appendChild(dragImage);

    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setDragImage(dragImage, e.offsetX, e.offsetY);
    e.dataTransfer.setData('text/html', this.outerHTML);

    // Remove the temporary drag image after a short delay
    setTimeout(() => {
      document.body.removeChild(dragImage);
    }, 0);
  }

  function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }

  function handleDragEnter(e) {
    e.preventDefault();
    if (this !== draggedElement) {
      // Remove drag-over from all other items first
      priorityItems.forEach(item => {
        if (item !== this) item.classList.remove('drag-over');
      });
      this.classList.add('drag-over');
    }
  }

  function handleDragLeave(e) {
    // Only remove if we're actually leaving the element (not entering a child)
    if (!this.contains(e.relatedTarget)) {
      this.classList.remove('drag-over');
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();

    console.log('Drop event fired', { draggedElement, target: this });

    // Ensure we have a valid dragged element
    if (!draggedElement || !draggedElement.parentNode) {
      console.error('Invalid dragged element:', draggedElement);
      this.classList.remove('drag-over');
      return;
    }

    console.log('Dragged element is valid, proceeding with drop');

    if (this !== draggedElement) {
      const allItems = Array.from(priorityGrid.querySelectorAll('.priority-item'));
      const draggedIndex = allItems.indexOf(draggedElement);
      const targetIndex = allItems.indexOf(this);

      console.log('Indices:', { draggedIndex, targetIndex, draggedElement, target: this });

      // Add reordering animation class
      priorityItems.forEach(item => {
        if (item !== draggedElement) {
          item.classList.add('reordering');
        }
      });

      // Perform DOM manipulation immediately (no delay for debugging)
      if (draggedIndex < targetIndex) {
        console.log('Inserting before next sibling');
        this.parentNode.insertBefore(draggedElement, this.nextSibling);
      } else {
        console.log('Inserting before target');
        this.parentNode.insertBefore(draggedElement, this);
      }

      // Update priority numbers
      updatePriorityNumbers();

      // Remove reordering animation after transition
      setTimeout(() => {
        priorityItems.forEach(item => {
          item.classList.remove('reordering');
        });
      }, 400);
    }

    this.classList.remove('drag-over');
  }

  function handleDragEnd(e) {
    console.log('Drag end fired for:', this);
    this.classList.remove('dragging');

    // Clean up all drag states
    priorityItems.forEach(item => {
      item.classList.remove('drag-over', 'reordering');
    });

    console.log('Resetting draggedElement from:', draggedElement);
    draggedElement = null;
    console.log('DraggedElement is now:', draggedElement);

    // Add subtle success animation
    this.style.animation = 'none';
    this.offsetHeight; // Trigger reflow
    this.style.animation = 'floatUp 0.6s ease-out';
    setTimeout(() => {
      this.style.animation = '';
    }, 600);
  }

  // Touch event handlers for mobile support
  function handleTouchStart(e) {
    if (e.touches.length === 1) {
      const touch = e.touches[0];
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
      draggedElement = this;

      // Add visual feedback
      this.classList.add('dragging');

      // Haptic feedback if available
      if (navigator.vibrate) {
        navigator.vibrate(50);
      }
    }
  }

  function handleTouchMove(e) {
    if (!draggedElement || e.touches.length !== 1) return;

    e.preventDefault();
    const touch = e.touches[0];
    const deltaX = Math.abs(touch.clientX - touchStartX);
    const deltaY = Math.abs(touch.clientY - touchStartY);

    // Only start dragging if moved significantly (prevent accidental drags)
    if (deltaX > 10 || deltaY > 10) {
      const elementsAtPoint = document.elementsFromPoint(touch.clientX, touch.clientY);
      const priorityItem = elementsAtPoint.find(el =>
        el.classList.contains('priority-item') && el !== draggedElement
      );

      // Clear previous drag-over states
      priorityItems.forEach(item => item.classList.remove('drag-over'));

      // Add drag-over to target item
      if (priorityItem) {
        priorityItem.classList.add('drag-over');
      }
    }
  }

  function handleTouchEnd(e) {
    if (!draggedElement || !draggedElement.parentNode) return;

    const touch = e.changedTouches[0];
    const elementsAtPoint = document.elementsFromPoint(touch.clientX, touch.clientY);
    const targetItem = elementsAtPoint.find(el =>
      el.classList.contains('priority-item') && el !== draggedElement
    );

    if (targetItem) {
      // Perform the reordering
      const allItems = Array.from(priorityGrid.querySelectorAll('.priority-item'));
      const draggedIndex = allItems.indexOf(draggedElement);
      const targetIndex = allItems.indexOf(targetItem);

      // Add reordering animation
      priorityItems.forEach(item => {
        if (item !== draggedElement) {
          item.classList.add('reordering');
        }
      });

      setTimeout(() => {
        if (draggedIndex < targetIndex) {
          targetItem.parentNode.insertBefore(draggedElement, targetItem.nextSibling);
        } else {
          targetItem.parentNode.insertBefore(draggedElement, targetItem);
        }

        updatePriorityNumbers();

        setTimeout(() => {
          priorityItems.forEach(item => {
            item.classList.remove('reordering');
          });
        }, 400);
      }, 50);

      // Haptic feedback for successful drop
      if (navigator.vibrate) {
        navigator.vibrate([30, 50, 30]);
      }
    }

    // Clean up
    priorityItems.forEach(item => {
      item.classList.remove('drag-over', 'dragging', 'reordering');
    });

    draggedElement = null;

    // Success animation
    if (targetItem) {
      this.style.animation = 'floatUp 0.6s ease-out';
      setTimeout(() => {
        this.style.animation = '';
      }, 600);
    }
  }

  function updatePriorityNumbers() {
    const items = priorityGrid.querySelectorAll('.priority-item');
    items.forEach((item, index) => {
      const numberSpan = item.querySelector('.priority-number');
      if (numberSpan) {
        numberSpan.textContent = (index + 1).toString();
        item.setAttribute('data-priority', index + 1);
      }
    });

    // Save the new priority order to localStorage
    savePriorityOrder();
  }

  function savePriorityOrder() {
    const items = priorityGrid.querySelectorAll('.priority-item');
    const priorityOrder = Array.from(items).map(item => {
      return {
        priority: item.getAttribute('data-priority'),
        text: item.querySelector('.priority-text').textContent,
        icon: item.querySelector('.priority-icon').textContent
      };
    });
    localStorage.setItem('priorityOrder', JSON.stringify(priorityOrder));
  }

  // Load saved priority order on page load
  function loadPriorityOrder() {
    const savedOrder = localStorage.getItem('priorityOrder');
    if (savedOrder) {
      try {
        const priorityOrder = JSON.parse(savedOrder);
        // Reorder elements based on saved order
        priorityOrder.forEach((saved, index) => {
          const items = priorityGrid.querySelectorAll('.priority-item');
          const currentItem = Array.from(items).find(item => 
            item.querySelector('.priority-text').textContent === saved.text
          );
          if (currentItem && index < items.length) {
            priorityGrid.appendChild(currentItem);
          }
        });
        updatePriorityNumbers();
      } catch (e) {
        console.log('Could not load saved priority order');
      }
    }
  }

  // Load saved order on initialization
  loadPriorityOrder();
}
