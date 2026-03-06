<template>
  <div class="doctor-details-page">
    <div class="profile-card">
      <!-- COMPACT HEADER -->
      <div class="profile-header">
        <div class="doctor-avatar">
          <i class="bi bi-person-heart"></i>
        </div>
        <div class="header-text">
          <h2>{{ doc_name || 'Loading...' }}</h2>
          <span class="dept-tag">{{ doctors.department_name }}</span>
        </div>
      </div>

      <!-- COMPACT INFO GRID -->
      <div class="info-grid">
        <div class="info-item">
          <span class="label">Specialty</span>
          <span class="value">{{ doctors.specialty }}</span>
        </div>
        <div class="info-item">
          <span class="label">Gender</span>
          <span class="value">{{ doctors.gender }}</span>
        </div>
        <div class="info-item">
          <span class="label">Age</span>
          <span class="value">{{ doctors.age }} yrs</span>
        </div>
        <div class="info-item">
          <span class="label">Contact</span>
          <span class="value">{{ doctors.contact_number }}</span>
        </div>
        <div class="info-item full">
          <span class="label">Address</span>
          <span class="value">{{ doctors.address }}</span>
        </div>
      </div>

      <!-- DESCRIPTION & BUTTONS -->
      <div class="bottom-section">
        <div class="description">
          <span class="label">About</span>
          <p>{{ doctors.description }}</p>
        </div>
        
        <div class="action-buttons">
          <RouterLink :to="`/department_details/${dept_id}`" class="btn btn-back">
            <i class="bi bi-arrow-left"></i> Back
          </RouterLink>
          <RouterLink :to="`/appointment/${doctors.department_name}/${doctors.id}`" class="btn btn-book">
            <i class="bi bi-calendar-check"></i> Book
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Doctor_details",
  data() {
    return {
      token: "",
      doctors: {},
      doc_name: "",
      dept_id: null
    };
  },
  mounted() {
    this.tokenload();
    this.doctor_details();
  },
  methods: {
    tokenload() {
      const token = localStorage.getItem("token");
      if (token) this.token = token;
    },
    async doctor_details() {
      try {
        const doc_id = this.$route.params.id;
        const response = await axios.get(`http://127.0.0.1:5000/api/doctor_details/${doc_id}`, {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": this.token
          }
        });
        this.doctors = response.data.doctor;
        this.dept_id = response.data.dept_id;
        this.doc_name = response.data.doctor.name;
      } catch (err) {
        console.error('Error:', err);
      }
    }
  }
}
</script>

<style scoped>
.doctor-details-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
  font-family: 'Inter', sans-serif;
}

.profile-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 0 auto;
  overflow: hidden;
}

.profile-header {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.doctor-avatar {
  width: 60px;
  height: 60px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.header-text h2 {
  margin: 0 0 0.25rem 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.dept-tag {
  background: rgba(255,255,255,0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.info-grid {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem;
  background: rgba(255,255,255,0.7);
  border-radius: 12px;
  border-left: 3px solid #10b981;
}

.info-item.full {
  grid-column: span 2;
}

.label {
  font-size: 0.8rem;
  color: #059669;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
}

.bottom-section {
  padding: 0 1.5rem 1.5rem;
}

.description {
  margin-bottom: 1.5rem;
}

.description .label {
  display: block;
  margin-bottom: 0.5rem;
}

.description p {
  margin: 0;
  color: #475569;
  line-height: 1.5;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.btn {
  flex: 1;
  padding: 0.9rem 1rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-back {
  background: #6b7280;
  color: white;
}

.btn-book {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16,185,129,0.3);
}

@media (max-width: 768px) {
  .doctor-details-page {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>
