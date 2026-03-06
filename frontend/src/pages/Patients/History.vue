<template>
  <div class="treatment-history-container">
    <!-- PAGE HEADER -->
    <div class="page-header">
      <h2>Treatment History</h2>
    </div>
    
    <!-- PATIENT INFO + STATS - MADE SMALLER -->
    <div class="patient-info-section">
      <div class="patient-info-card">
        <div class="info-item">
          <span class="info-label">Name:</span>
          <span class="info-value">{{ name || 'Loading...' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Gender:</span>
          <span class="info-value">{{ gender }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Age:</span>
          <span class="info-value">{{ age }} years</span>
        </div>
        <div class="info-item highlight">
          <span class="info-label">Total Visits:</span>
          <span class="info-value">{{ appointments?.length || 0 }}</span>
        </div>
      </div>
    </div>

    <!-- TREATMENT TABLE -->
    <div class="table-container">
      <div class="table-responsive">
        <table v-if="status_code === 404 || !appointments?.length" class="empty-table">
          <tbody>
            <tr>
              <td class="no-data">No Treatment History Available</td>
            </tr>
          </tbody>
        </table>
        
        <table v-else class="treatment-table">
          <thead>
            <tr>
              <th>Doctor</th>
              <th>Department</th>
              <th>Date</th>
              <th>Time</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Tests</th>
              <th>Medicines</th>
              <th>Visit Type</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in appointments" :key="record.id" class="treatment-row">
              <td>{{ record.doctor_name }}</td>
              <td>{{ record.department_name }}</td>
              <td>{{ formatDate(record.date) }}</td>
              <td>{{ record.time }}</td>
              <td>{{ record.diagnosis || 'N/A' }}</td>
              <td>{{ record.prescription || 'N/A' }}</td>
              <td>{{ record.test_done || 'None' }}</td>
              <td>{{ record.medicines || 'N/A' }}</td>
              <td>{{ record.visit_type }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "PatientHistory",
  data() {
    return {
      token: "",
      name: "",
      gender: "",
      age: "",
      appointments: [],
      id: "",
      status_code: null
    };
  },
  mounted() {
    this.tokenload();
    const id = this.$route.params.id;
    this.id = id;
    this.fetchinghistory();
  },
  methods: {
    tokenload() {
      const token = localStorage.getItem("token");
      if (token) this.token = token;
    },
    async fetchinghistory() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/patient_history/${this.id}`, {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": this.token,
          }
        });
        
        this.gender = response.data.patient_gender || '';
        this.age = response.data.patient_age || '';
        this.status_code = response.data.status_code;
        this.name = response.data.patient_name || '';
        
        if (response.data.status_code === 404) {
          this.appointments = [];
        } else {
          this.appointments = response.data.treatments || [];
        }
      } catch (error) {
        console.error('Error fetching history:', error);
        this.appointments = [];
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric'
      });
    }
  }
}
</script>

<style scoped>
.treatment-history-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
  padding: 2.5rem 2rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* SMALLER HEADER (already adjusted) */
.page-header {
  text-align: center;
  margin-bottom: 1.5rem; /* Further reduced */
}

.page-header h2 {
  color: #581c87;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa, #c4b5fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.page-header h2::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 2px;
}

/* SMALLER PATIENT INFO CARD (SECOND BLOCK) */
.patient-info-section {
  margin-bottom: 1.5rem; /* Reduced from 2rem */
}

.patient-info-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px; /* Smaller radius: 20px → 16px */
  padding: 1.25rem 1.5rem; /* Smaller padding: 2rem → 1.25rem/1.5rem */
  box-shadow: 0 15px 30px rgba(0,0,0,0.08); /* Lighter shadow */
  border: 1px solid rgba(139,92,246,0.15); /* Thinner border */
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); /* Tighter columns */
  gap: 1rem; /* Reduced gap: 1.5rem → 1rem */
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem; /* Smaller gap */
}

.info-label {
  font-size: 0.85rem; /* Smaller: 0.95rem → 0.85rem */
  font-weight: 600;
  color: #6b21a8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1.1rem; /* Smaller: 1.3rem → 1.1rem */
  font-weight: 700;
  color: #1e293b;
}

.info-item.highlight {
  background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(167,139,250,0.08) 100%);
  padding: 1rem; /* Smaller padding */
  border-radius: 10px; /* Smaller radius */
  border-left: 3px solid #8b5cf6; /* Thinner border */
}

.table-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 25px 50px rgba(0,0,0,0.15);
  border: 1px solid rgba(139,92,246,0.25);
  max-height: 75vh;
  overflow: hidden;
}

.table-responsive {
  overflow-x: auto;
  max-height: 65vh;
  overflow-y: auto;
}

.treatment-table,
.empty-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 1rem;
}

.treatment-table thead,
.empty-table thead {
  position: sticky;
  top: 0;
  z-index: 10;
}

.treatment-table th {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 50%, #5b21b6 100%);
  color: white;
  padding: 1.5rem 1.25rem;
  text-align: left;
  font-weight: 700;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border-bottom: 3px solid rgba(255,255,255,0.2);
  box-shadow: 0 2px 10px rgba(118,44,217,0.3);
}

.treatment-table th:first-child {
  border-radius: 20px 0 0 0;
}

.treatment-table th:last-child {
  border-radius: 0 20px 0 0;
}

.treatment-row {
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
  cursor: pointer;
  position: relative;
}

.treatment-row:hover {
  background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(167,139,250,0.08) 100%);
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(139,92,246,0.15);
}

.treatment-row td {
  padding: 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(139,92,246,0.1);
  color: #581c87;
  font-weight: 500;
  vertical-align: middle;
}

.treatment-row td:last-child {
  white-space: nowrap;
}

.no-data {
  text-align: center;
  color: #8b5cf6;
  font-size: 1.2rem;
  font-weight: 600;
  padding: 4rem 2rem;
  font-style: italic;
}

/* CUSTOM SCROLLBAR */
.table-responsive::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.table-responsive::-webkit-scrollbar-track {
  background: rgba(226,232,240,0.5);
  border-radius: 10px;
}

.table-responsive::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(139,92,246,0.3);
}

.table-responsive::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c3aed, #9333ea);
}

/* RESPONSIVE */
@media (max-width: 992px) {
  .treatment-history-container {
    padding: 2rem 1.5rem;
  }
  
  .patient-info-card {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 0.75rem; /* Smaller gap on tablet */
    padding: 1rem 1.25rem;
  }
}

@media (max-width: 768px) {
  .treatment-history-container {
    padding: 1.5rem 1rem;
  }
  
  .page-header h2 {
    font-size: 1.8rem;
  }
  
  .patient-info-card {
    padding: 1rem;
    gap: 0.75rem;
  }
  
  .info-value {
    font-size: 1rem; /* Even smaller on mobile */
  }
  
  .table-container {
    padding: 1.5rem;
  }
  
  .treatment-table {
    font-size: 0.9rem;
  }
  
  .treatment-table th,
  .treatment-row td {
    padding: 1rem 0.75rem;
  }
  
  /* MOBILE CARD VIEW */
  .treatment-table thead {
    display: none;
  }
  
  .treatment-row {
    display: block;
    margin-bottom: 1.5rem;
    border: 2px solid rgba(139,92,246,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 8px 25px rgba(139,92,246,0.15);
    transition: all 0.3s ease;
  }
  
  .treatment-row:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(139,92,246,0.25);
  }
  
  .treatment-row td {
    display: block;
    border: none !important;
    padding: 0.75rem 0;
    position: relative;
    padding-left: 45%;
    font-size: 1rem;
  }
  
  .treatment-row td:before {
    content: attr(data-label) ": ";
    position: absolute;
    left: 0;
    width: 40%;
    font-weight: 700;
    color: #6b21a8;
    font-size: 0.95rem;
  }
}
</style>
