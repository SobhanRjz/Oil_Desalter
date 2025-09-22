// Handle CTA click, demo API call, and video performance tweaks

const cta = document.getElementById('cta');
const video = document.getElementById('bg-video');

// Video loading and error handling
if (video) {
    console.log('Video element found, setting up event listeners');

    video.addEventListener('error', (e) => {
        console.log('Video failed to load:', e);
        console.log('Video error code:', video.error?.code);
        console.log('Video error message:', video.error?.message);
        video.style.display = 'none';
        const fallback = document.getElementById('fallback-image');
        if (fallback) {
            console.log('Showing fallback image');
            fallback.style.display = 'block';
        } else {
            console.log('Fallback image not found');
        }
    });

    video.addEventListener('loadstart', () => {
        console.log('Video loading started');
    });

    video.addEventListener('canplay', () => {
        console.log('Video can play');
    });

    video.addEventListener('loadeddata', () => {
        console.log('Video data loaded');
    });

    // Check if video is already loaded
    if (video.readyState >= 3) {
        console.log('Video already loaded');
    }
}

// Pause the video when the tab is hidden to save resources
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { video?.pause(); }
  else { video?.play().catch(()=>{}); }
});

cta?.addEventListener('click', (e) => {
  e.preventDefault();
  cta.classList.add('loading');
  cta.textContent = 'Loading...';

  // Navigate to login page after a short delay for smooth UX
  setTimeout(() => {
    window.location.href = '/login';
  }, 800);
});
