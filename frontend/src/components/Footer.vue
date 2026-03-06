<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-main">
        <div class="footer-logo">
          <i class="fas fa-leaf"></i>
          <span>Ayurveda Hospital</span>
        </div>
        <p class="footer-text">
          © 2026 Ayurveda Hospital. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.footer {
  background: linear-gradient(135deg, #1e1b4b 0%, #2a1a4e 50%, #4a1f6f 100%);
  color: white;
  position: relative;
  overflow: hidden;
  box-shadow: 0 -4px 20px rgba(74, 31, 111, 0.3);
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #a855f7, transparent);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 2.5rem;
  position: relative;
  z-index: 1;
}

.footer-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #e879f9;
  text-shadow: 0 2px 8px rgba(232, 121, 249, 0.3);
}

.footer-logo i {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #e879f9, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-text {
  margin: 0;
  opacity: 0.9;
  font-size: 0.95rem;
  font-weight: 400;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.85rem;
}

.footer-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.footer-link:hover {
  color: #e879f9;
  text-shadow: 0 0 10px rgba(232, 121, 249, 0.5);
}

.footer-link + span {
  color: rgba(255, 255, 255, 0.4);
  font-weight: 300;
}

.footer-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.footer-badge i {
  color: #ef4444;
  animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@media (max-width: 768px) {
  .footer-content {
    padding: 1.5rem 1rem;
    flex-direction: column;
    text-align: center;
  }
  
  .footer-main {
    justify-content: center;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
