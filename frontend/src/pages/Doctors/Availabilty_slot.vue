<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-11 col-lg-10">
        <div class="card shadow-lg">
          <div class="card-header bg-success text-white text-center py-4">
            <h3>🩺 Set Weekly Availability</h3>
            <p class="mb-0">15 slots/day × 7 days (Today + 6 days ahead)</p>
          </div>
          <div class="card-body p-4">
            
            <!-- DATE TABS (7 DAYS) -->
            <div class="mb-4">
              <label class="form-label fw-bold fs-5 mb-3">Select Date <span class="text-danger">*</span></label>
              <div class="btn-group w-100" role="group">
                <button v-for="day in weekDays" :key="day.date" class="btn btn-outline-primary day-btn fs-6"
                  :class="{ 'btn-primary text-white active': selectedDate === day.date }" @click="selectDate(day.date)">
                  <strong>{{ day.dayName }}</strong><br> <small>{{ day.date }}</small>
                </button>
              </div>
            </div>

            <!-- 3 PERIODS × 5 SLOTS (15 TOTAL) -->
            <div v-if="selectedDate" class="availability-section">
              <h5 class="fw-bold mb-4 text-success">
                📅 {{ selectedDayName }} ({{ selectedDate }})
              </h5>
              
              <!-- MORNING: 9AM, 10AM, 11AM, 12PM, 1PM -->
              <div class="period-section mb-5">
                <h6 class="bg-warning text-dark p-3 rounded-top fw-bold mb-0">
                  🌅 MORNING (9AM - 1PM) - 5 Slots
                </h6>
                <div class="row g-3 p-3 bg-light rounded-bottom">
                  <div v-for="slot in morningSlots" :key="slot.time" class="col-md-2 col-sm-4 col-6">
                    <div class="slot-card">
                      <div class="form-check form-switch d-flex align-items-center">
                        <input class="form-check-input me-2" type="checkbox" :id="`morning-${selectedDate}-${slot.time}`"
                          v-model="availability[selectedDate].morning[slot.time]">
                        <label class="form-check-label d-block w-100 cursor-pointer" :for="`morning-${selectedDate}-${slot.time}`">
                          <strong>{{ slot.display }}</strong>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- AFTERNOON: 2PM, 2:30PM, 3PM, 4PM, 5PM -->
              <div class="period-section mb-5">
                <h6 class="bg-info text-white p-3 rounded-top fw-bold mb-0">
                  ☀️ AFTERNOON (2PM - 5PM) - 5 Slots
                </h6>
                <div class="row g-3 p-3 bg-light rounded-bottom">
                  <div v-for="slot in afternoonSlots" :key="slot.time" class="col-md-2 col-sm-4 col-6">
                    <div class="slot-card">
                      <div class="form-check form-switch d-flex align-items-center">
                        <input 
                          class="form-check-input me-2" 
                          type="checkbox" 
                          :id="`afternoon-${selectedDate}-${slot.time}`"
                          v-model="availability[selectedDate].afternoon[slot.time]"
                        >
                        <label class="form-check-label d-block w-100 cursor-pointer" :for="`afternoon-${selectedDate}-${slot.time}`">
                          <strong>{{ slot.display }}</strong>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- EVENING: 6PM, 6:30PM, 7PM, 7:30PM, 8PM -->
              <div class="period-section mb-5">
                <h6 class="bg-danger text-white p-3 rounded-top fw-bold mb-0">
                  🌙 EVENING (6PM - 8PM) - 5 Slots
                </h6>
                <div class="row g-3 p-3 bg-light rounded-bottom">
                  <div v-for="slot in eveningSlots" :key="slot.time" class="col-md-2 col-sm-4 col-6">
                    <div class="slot-card">
                      <div class="form-check form-switch d-flex align-items-center">
                        <input 
                          class="form-check-input me-2" 
                          type="checkbox" 
                          :id="`evening-${selectedDate}-${slot.time}`"
                          v-model="availability[selectedDate].evening[slot.time]"
                        >
                        <label class="form-check-label d-block w-100 cursor-pointer" :for="`evening-${selectedDate}-${slot.time}`">
                          <strong>{{ slot.display }}</strong>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- SUMMARY & SAVE -->
              <div class="row mt-5">
                <div class="col-md-6">
                  <div class="alert alert-success">
                    <h5>📊 Today’s Summary:</h5>
                    <!-- <p class="mb-2"><strong>{{ totalAvailableSlots }} / 15 slots available</strong></p> -->
                    <small class="text-muted">
                      Morning: {{ morningCount }} | Afternoon: {{ afternoonCount }} | Evening: {{ eveningCount }}
                    </small>
                  </div>
                </div>
                <div class="col-md-6 text-end">
                  <button class="btn btn-success btn-lg px-5 me-2" @click="saveAvailability" :disabled="!hasChanges">
                    💾 Save All Changes
                  </button>
                  <button class="btn btn-outline-secondary btn-lg px-5" @click="resetAll">
                    🔄 Reset
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-center mt-4">
          <RouterLink to="/doctor_dash" class="btn btn-primary btn-lg">← Back to Dashboard</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DoctorWeeklyAvailability',
  data() {
    return {
      selectedDate: '',
      token: '',
      user_type: '',
      availability: {},  // Will be populated in initializeAvailability
      originalAvailability: {},
      weekDays: [],
      morningSlots: [
        { time: '09:00', display: '9:00 ' },
        { time: '10:00', display: '10:00 ' },
        { time: '11:00', display: '11:00 ' },
        { time: '12:00', display: '12:00 ' },
        { time: '13:00', display: '13:00 ' }
      ],
      afternoonSlots: [
        { time: '14:00', display: '14:00 ' },
        { time: '14:30', display: '14:30 ' },
        { time: '15:00', display: '15:00 ' },
        { time: '16:00', display: '16:00 ' },
        { time: '17:00', display: '17:00 ' }
      ],
      eveningSlots: [
        { time: '18:00', display: '18:00 ' },
        { time: '18:30', display: '18:30 ' },
        { time: '19:00', display: '19:00 ' },
        { time: '19:30', display: '19:30 ' },
        { time: '20:00', display: '20:00 ' }
      ]
    }
  },
  computed: {
    selectedDayName() {
      return this.weekDays.find(day => day.date === this.selectedDate)?.dayName || '';
    },
    morningCount() {
      const dayData = this.availability[this.selectedDate];
      return dayData?.morning ? Object.values(dayData.morning).filter(Boolean).length : 0;
    },
    afternoonCount() {
      const dayData = this.availability[this.selectedDate];
      return dayData?.afternoon ? Object.values(dayData.afternoon).filter(Boolean).length : 0;
    },
    eveningCount() {
      const dayData = this.availability[this.selectedDate];
      return dayData?.evening ? Object.values(dayData.evening).filter(Boolean).length : 0;
    },
    hasChanges() {
      return JSON.stringify(this.availability) !== JSON.stringify(this.originalAvailability);
    }
  },
  mounted() {
    this.tokenload();
    this.generateWeekDays();
    this.initializeAvailability();  // ✅ FIX: Initialize structure
    this.loadAvailability();  // Load existing availability from backend
  },
  methods: {
    tokenload() {
      const token = localStorage.getItem("token");
      if (token) this.token = token;
      const user_type = localStorage.getItem('user_type');
      if (user_type) this.user_type = user_type;
    },
    generateWeekDays() {
      const today = new Date();
      const days = [];
      for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        days.push({
          date: date.toISOString().split('T')[0],
          dayName: date.toLocaleDateString('en-US', { weekday: 'long' })
        });
      }
      this.weekDays = days;
      this.selectedDate = days[0].date;
    },
    initializeAvailability() {
      // ✅ FIX: Create full structure BEFORE template renders
      this.weekDays.forEach(day => {
        if (!this.availability[day.date]) {
          this.availability[day.date] = {
            morning: {
              '09:00': false, '10:00': false, '11:00': false,
              '12:00': false, '13:00': false
            },
            afternoon: {
              '14:00': false, '14:30': false, '15:00': false,
              '16:00': false, '17:00': false
            },
            evening: {
              '18:00': false, '18:30': false, '19:00': false,
              '19:30': false, '20:00': false
            }
          };
        }
      });
      this.originalAvailability = JSON.parse(JSON.stringify(this.availability));
      console.log('✅ Availability initialized:', this.availability);
    },
    selectDate(date) {
      this.selectedDate = date;
    },
    async saveAvailability() {
      const doctor_id = this.$route.params?.doctor_id || 1; // Fallback
      try {
        await axios.post(`http://127.0.0.1:5000/api/add_available_slot/${doctor_id}`, 
          this.availability, {
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.token
          }
        });
        this.originalAvailability = JSON.parse(JSON.stringify(this.availability));
        console.log('✅ Availability saved:', this.availability);
        alert('✅ availability saved successfully!');
      } catch (error) {
        alert('❌ Save failed');
        console.error(error);
      }
    },
    resetAll() {
      this.availability = JSON.parse(JSON.stringify(this.originalAvailability));
    },
    async loadAvailability() {
      const doctor_id = this.$route.params?.doctor_id || 1;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/doctor_available_slots/${doctor_id}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': this.token
          }
        });
        
        const slotsList = response.data.available_slots;  // ✅ Flat list from backend
        
        // ✅ Transform flat list → nested structure
        const nestedAvailability = {};
        
        // Initialize all dates/periods first
        this.weekDays.forEach(day => {
          nestedAvailability[day.date] = {
            morning: { '09:00': false, '10:00': false, '11:00': false, '12:00': false, '13:00': false },
            afternoon: { '14:00': false, '14:30': false, '15:00': false, '16:00': false, '17:00': false },
            evening: { '18:00': false, '18:30': false, '19:00': false, '19:30': false, '20:00': false }
          };
        });
        
        // Map backend slots to nested structure
        slotsList.forEach(slot => {
          const dateKey = slot.date;
          const timeKey = slot.start_time;
          
          // Find which period the time belongs to
          let period = null;
          if (['09:00', '10:00', '11:00', '12:00', '13:00'].includes(timeKey)) {
            period = 'morning';
          } else if (['14:00', '14:30', '15:00', '16:00', '17:00'].includes(timeKey)) {
            period = 'afternoon';
          } else if (['18:00', '18:30', '19:00', '19:30', '20:00'].includes(timeKey)) {
            period = 'evening';
          }
          
          if (period && nestedAvailability[dateKey]) {
            nestedAvailability[dateKey][period][timeKey] = slot.is_available;
          }
        });
        
        this.availability = nestedAvailability;
        this.originalAvailability = JSON.parse(JSON.stringify(nestedAvailability));
        console.log('✅ Transformed availability:', this.availability);
        
      } catch (error) {
        console.error('Load failed:', error);
        this.error = 'Failed to load availability';
      }
    }

  }
}
</script>


<style scoped>
.day-btn {
  height: 80px;
  border-radius: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 2px solid #dee2e6;
}

.day-btn:hover:not(.active), .day-btn.active {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,123,255,0.3);
}

.period-section {
  border: 2px solid #e9ecef;
  border-radius: 15px;
  overflow: hidden;
}

.slot-card {
  background: white;
  border-radius: 10px;
  padding: 12px;
  border: 2px solid #f8f9fa;
  transition: all 0.2s ease;
  cursor: pointer;
}

.slot-card:hover {
  border-color: #28a745;
  box-shadow: 0 4px 12px rgba(40,167,69,0.15);
}

.cursor-pointer {
  cursor: pointer;
}

.card {
  border: none;
  border-radius: 25px;
  overflow: hidden;
}
</style>
