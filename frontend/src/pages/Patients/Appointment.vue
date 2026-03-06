<template>
  <div class="appointment-booking">
    <div class="booking-card">
      <!-- HEADER -->
      <div class="booking-header">
        <div class="doctor-info">
          <div class="avatar">
            <i class="bi-person-heart"></i>
          </div>
          <div>
            <h2>Book Appointment</h2>
            <p>{{ doc_name }}</p>
          </div>
        </div>
      </div>

      <!-- CONTENT -->
      <div class="booking-content">
        <!-- ERROR -->
        <div v-if="error" class="error-alert">
          {{ error }}
        </div>

        <!-- LOADING -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading slots...</p>
        </div>

        <!-- DATE SELECTOR -->
        <div v-else class="date-section">
          <label>Select Date</label>
          <input type="date" v-model="selectedDate" :min="minDate" @change="loadAvailableSlots" class="date-input"/>
        </div>

        <!-- TIME SLOTS -->
        <div v-if="selectedDate && !loading && availableSlots.length" class="slots-section">
          <div class="slots-header">
            <h4>{{ availableSlots.length }} Available Slots</h4>
          </div>

          <!-- MORNING -->
          <div v-if="morningAvailableSlots.length" class="slot-group">
            <h5>🕐 Morning</h5>
            <div class="slot-buttons">
              <button 
                v-for="slot in morningAvailableSlots" 
                :key="slot.start_time"
                class="slot-btn"
                :class="{ 'selected': selectedSlot === slot.start_time }"
                @click="selectSlot(slot.start_time)"
              >
                {{ formatTime(slot.start_time) }}
              </button>
            </div>
          </div>

          <!-- AFTERNOON -->
          <div v-if="afternoonAvailableSlots.length" class="slot-group">
            <h5>🌞 Afternoon</h5>
            <div class="slot-buttons">
              <button 
                v-for="slot in afternoonAvailableSlots" 
                :key="slot.start_time"
                class="slot-btn"
                :class="{ 'selected': selectedSlot === slot.start_time }"
                @click="selectSlot(slot.start_time)"
              >
                {{ formatTime(slot.start_time) }}
              </button>
            </div>
          </div>

          <!-- EVENING -->
          <div v-if="eveningAvailableSlots.length" class="slot-group">
            <h5>🌙 Evening</h5>
            <div class="slot-buttons">
              <button 
                v-for="slot in eveningAvailableSlots" 
                :key="slot.start_time"
                class="slot-btn"
                :class="{ 'selected': selectedSlot === slot.start_time }"
                @click="selectSlot(slot.start_time)"
              >
                {{ formatTime(slot.start_time) }}
              </button>
            </div>
          </div>

          <!-- SUMMARY & BOOK -->
          <div v-if="selectedSlot" class="booking-summary">
            <div class="summary-card">
              <h4>✅ Confirmed</h4>
              <p>{{ selectedDate }} at {{ formatTime(selectedSlot) }}</p>
              <p class="doctor">{{ doc_name }}</p>
            </div>
            <button class="book-btn" @click="bookAppointment">
              <i class="fas fa-check"></i>
              Book Now
            </button>
          </div>
        </div>

        <!-- NO SLOTS -->
        <div v-if="selectedDate && availableSlots.length === 0" class="no-slots">
          <i class="fas fa-calendar-times"></i>
          <h4>No slots available</h4>
          <p>Try another date</p>
        </div>
      </div>

      <!-- BACK BUTTON -->
      <div class="back-btn-container">
        <RouterLink :to="`/department_details/${departmentId}`" class="back-btn">
          ← Back to Department
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Appointment',
  data() {
    return {
      selectedDate: '',
      selectedSlot: '',
      token: '',
      user_type: '',
      loading: false,
      error: '',
      minDate: new Date().toISOString().split('T')[0],
      availableSlots: [],
      departmentName: '',
      doc_name: "",
      departmentId: null,
      formData: {
        doctor: '',
        date: '',
        time: '',
        department_name: ''
      }
    }
  },
  computed: {
    morningAvailableSlots() {
      return this.availableSlots.filter(slot => {
        const hour = slot.start_time.split(':')[0];
        return hour >= 9 && hour <= 13;
      });
    },
    afternoonAvailableSlots() {
      return this.availableSlots.filter(slot => {
        const hour = slot.start_time.split(':')[0];
        return hour >= 14 && hour <= 17;
      });
    },
    eveningAvailableSlots() {
      return this.availableSlots.filter(slot => {
        const hour = slot.start_time.split(':')[0];
        return hour >= 18 && hour <= 20;
      });
    }
  },
  mounted() {
    this.tokenload();
    this.loadinfo();
    this.departmentName = this.$route.params.department || '';
    this.formData.department_name = this.departmentName;
  },
  methods: {
    tokenload() {
      this.token = localStorage.getItem('token') || '';
      this.user_type = localStorage.getItem('user_type') || '';
    },
    formatTime(time24) {
      const [hours, minutes] = time24.split(':');
      const time = new Date();
      time.setHours(parseInt(hours), parseInt(minutes));
      return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    loadinfo() {
      const doc_id = this.$route.params.doctor_id;
      const response = axios.get(`http://127.0.0.1:5000/api/doctor_details/${doc_id}`, {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": this.token,
          "user_type": this.user_type
        }
      });
      response.then(res => {
        this.formData.doctor = res.data.doctor.name;
        this.doc_name = res.data.doctor.name;
        this.departmentId = res.data.dept_id;
      }).catch(err => {
        this.error = err.response?.data?.message || 'Error loading doctor info';
      });
    },
    async loadAvailableSlots() {
      if (!this.selectedDate) return;
      this.loading = true;
      this.error = '';
      try {
        const doctorId = this.$route.params.doctor_id;
        const response = await axios.get(
          `http://127.0.0.1:5000/api/doctor_available_slots/${doctorId}?date=${this.selectedDate}`,
          { headers: { 'Authentication-Token': this.token } }
        );
        this.availableSlots = response.data.available_slots
          .filter(slot => slot.is_available)
          .map(slot => ({
            start_time: slot.start_time,
            date: slot.date
          }));
        this.formData.date = this.selectedDate;
        this.selectedSlot = '';
      } catch (error) {
        this.error = 'No slots available for this date';
        this.availableSlots = [];
      } finally {
        this.loading = false;
      }
    },
    selectSlot(slotTime) {
      this.selectedSlot = slotTime;
      this.formData.time = slotTime;
    },
    async bookAppointment() {
      if (!this.selectedSlot) {
        this.error = 'Please select a time slot';
        return;
      }
      try {
        await axios.post('http://127.0.0.1:5000/api/appointment', this.formData, {
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.token
          }
        });
        alert('✅ Appointment booked successfully!');
        this.$router.push('/patient_dash');
      } catch (error) {
        this.error = error.response?.data?.message || 'Booking failed';
      }
    }
  },
  watch: {
    selectedDate(newVal) {
      if (newVal) this.loadAvailableSlots();
    }
  }
}
</script>

<style scoped>
.appointment-booking {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
  font-family: 'Inter', sans-serif;
}

.booking-card {
  max-width: 550px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
}

.booking-header {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 1.5rem;
}

.doctor-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 50px;
  height: 50px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
}

.booking-header h2 {
  margin: 0 0 0.25rem 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.booking-header p {
  margin: 0;
  opacity: 0.9;
}

.booking-content {
  padding: 1.5rem;
}

.error-alert {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 12px;
  border-left: 4px solid #c33;
  margin-bottom: 1rem;
}

.loading-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.date-section {
  margin-bottom: 1.5rem;
}

.date-section label {
  display: block;
  font-weight: 600;
  color: #059669;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.date-input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.date-input:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.1);
}

.slots-header h4 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.slot-group {
  margin-bottom: 1.5rem;
}

.slot-group h5 {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-weight: 600;
}

.slot-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.slot-btn {
  padding: 0.6rem 1rem;
  border: 2px solid #d1d5db;
  background: white;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slot-btn:hover {
  transform: translateY(-1px);
  border-color: #10b981;
  box-shadow: 0 4px 12px rgba(16,185,129,0.2);
}

.slot-btn.selected {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-color: #10b981;
  box-shadow: 0 4px 15px rgba(16,185,129,0.4);
}

.no-slots {
  text-align: center;
  padding: 3rem 1rem;
  color: #94a3b8;
}

.no-slots i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.booking-summary {
  text-align: center;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-radius: 16px;
  border: 2px solid #10b981;
}

.summary-card h4 {
  margin: 0 0 0.5rem 0;
  color: #059669;
}

.summary-card p {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #1e293b;
}

.doctor {
  font-size: 0.9rem;
  color: #64748b;
}

.book-btn {
  width: 100%;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.book-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(16,185,129,0.4);
}

.back-btn-container {
  padding: 1.5rem;
  text-align: center;
  border-top: 1px solid rgba(226,232,240,0.5);
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: rgba(102,126,234,0.1);
  color: #667eea;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .appointment-booking {
    padding: 1rem;
  }
  
  .slot-buttons {
    justify-content: center;
  }
}
</style>
