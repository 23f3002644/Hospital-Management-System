<template>
  <div class="doctor-availability-page">
    <div class="availability-card">
      <!-- COMPACT HEADER -->
      <div class="availability-header">
        <div class="header-content">
          <div class="doctor-avatar">
            <i class="bi bi-hospital"></i>
          </div>
          <div>
            <h2>Set Availability</h2>
          </div>
        </div>
      </div>

      <!-- COMPACT DATE SELECTION -->
      <div class="date-selection">
        <div class="section-title">
          <i class="bi bi-calendar"></i> Select Date
        </div>
        <div class="date-grid">
          <button 
            v-for="day in weekDays" 
            :key="day.date"
            class="date-card"
            :class="{ active: selectedDate === day.date }"
            @click="selectDate(day.date)"
          >
            <div>{{ day.dayName.slice(0,3) }}</div>
            <div>{{ day.date.slice(8,10) }}</div>
          </button>
        </div>
      </div>

      <!-- SLOTS SECTION -->
      <div v-if="selectedDate" class="slots-section">
        <div class="current-date">
          <h4>{{ selectedDayName }} ({{ selectedDate.slice(5,10) }})</h4>
        </div>

        <!-- MORNING -->
        <div class="time-period morning">
          <div class="period-header">
            <span>🌅 Morning</span>
            <span class="count">{{ morningCount }}/5</span>
          </div>
          <div class="slots-grid">
            <div 
              v-for="slot in morningSlots"
              :key="slot.time"
              class="slot-item"
              :class="{ active: availability[selectedDate]?.morning[slot.time] }"
            >
              <input 
                type="checkbox"
                :id="`morning-${selectedDate}-${slot.time}`"
                v-model="availability[selectedDate].morning[slot.time]"
                class="slot-input"
              >
              <label :for="`morning-${selectedDate}-${slot.time}`" class="slot-label">
                {{ slot.display }}
              </label>
            </div>
          </div>
        </div>

        <!-- AFTERNOON -->
        <div class="time-period afternoon">
          <div class="period-header">
            <span>☀️ Afternoon</span>
            <span class="count">{{ afternoonCount }}/5</span>
          </div>
          <div class="slots-grid">
            <div 
              v-for="slot in afternoonSlots"
              :key="slot.time"
              class="slot-item"
              :class="{ active: availability[selectedDate]?.afternoon[slot.time] }"
            >
              <input 
                type="checkbox"
                :id="`afternoon-${selectedDate}-${slot.time}`"
                v-model="availability[selectedDate].afternoon[slot.time]"
                class="slot-input"
              >
              <label :for="`afternoon-${selectedDate}-${slot.time}`" class="slot-label">
                {{ slot.display }}
              </label>
            </div>
          </div>
        </div>

        <!-- EVENING -->
        <div class="time-period evening">
          <div class="period-header">
            <span>🌙 Evening</span>
            <span class="count">{{ eveningCount }}/5</span>
          </div>
          <div class="slots-grid">
            <div 
              v-for="slot in eveningSlots"
              :key="slot.time"
              class="slot-item"
              :class="{ active: availability[selectedDate]?.evening[slot.time] }"
            >
              <input 
                type="checkbox"
                :id="`evening-${selectedDate}-${slot.time}`"
                v-model="availability[selectedDate].evening[slot.time]"
                class="slot-input"
              >
              <label :for="`evening-${selectedDate}-${slot.time}`" class="slot-label">
                {{ slot.display }}
              </label>
            </div>
          </div>
        </div>

        <!-- SUMMARY & BUTTONS -->
        <div class="summary-actions">
          <div class="summary">
            Total: {{ totalAvailable }}/15
          </div>
          <div class="buttons">
            <button 
              class="btn save" 
              @click="saveAvailability"
              :disabled="!hasChanges"
            >
              Save
            </button>
            <button class="btn reset" @click="resetAll">
              Reset
            </button>
          </div>
        </div>
      </div>
    </div>

    <RouterLink to="/doctor_dash" class="back-btn">
      ← Back
    </RouterLink>
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
      availability: {},
      originalAvailability: {},
      weekDays: [],
      morningSlots: [
        { time: '09:00', display: '09:00' },
        { time: '10:00', display: '10:00' },
        { time: '11:00', display: '11:00' },
        { time: '12:00', display: '12:00' },
        { time: '13:00', display: '13:00' }
      ],
      afternoonSlots: [
        { time: '14:00', display: '14:00' },
        { time: '14:30', display: '14:30' },
        { time: '15:00', display: '15:00' },
        { time: '16:00', display: '16:00' },
        { time: '17:00', display: '17:00' }
      ],
      eveningSlots: [
        { time: '18:00', display: '18:00' },
        { time: '18:30', display: '18:30' },
        { time: '19:00', display: '19:00' },
        { time: '19:30', display: '19:30' },
        { time: '20:00', display: '20:00' }
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
    totalAvailable() {
      return this.morningCount + this.afternoonCount + this.eveningCount;
    },
    hasChanges() {
      return JSON.stringify(this.availability) !== JSON.stringify(this.originalAvailability);
    }
  },
  mounted() {
    this.tokenload();
    this.generateWeekDays();
    this.initializeAvailability();
    this.loadAvailability();
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
      this.weekDays.forEach(day => {
        if (!this.availability[day.date]) {
          this.availability[day.date] = {
            morning: { '09:00': false, '10:00': false, '11:00': false, '12:00': false, '13:00': false },
            afternoon: { '14:00': false, '14:30': false, '15:00': false, '16:00': false, '17:00': false },
            evening: { '18:00': false, '18:30': false, '19:00': false, '19:30': false, '20:00': false }
          };
        }
      });
      this.originalAvailability = JSON.parse(JSON.stringify(this.availability));
    },
    selectDate(date) {
      this.selectedDate = date;
    },
    async saveAvailability() {
      const doctor_id = this.$route.params?.doctor_id || 1;
      try {
        await axios.post(`http://127.0.0.1:5000/api/add_available_slot/${doctor_id}`, 
          this.availability, {
          headers: { 'Content-Type': 'application/json', 'Authentication-Token': this.token }
        });
        this.originalAvailability = JSON.parse(JSON.stringify(this.availability));
        alert('✅ Saved!');
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
          headers: { 'Content-Type': 'application/json', 'Authentication-Token': this.token }
        });
        const slotsList = response.data.available_slots;
        const nestedAvailability = {};
        this.weekDays.forEach(day => {
          nestedAvailability[day.date] = {
            morning: { '09:00': false, '10:00': false, '11:00': false, '12:00': false, '13:00': false },
            afternoon: { '14:00': false, '14:30': false, '15:00': false, '16:00': false, '17:00': false },
            evening: { '18:00': false, '18:30': false, '19:00': false, '19:30': false, '20:00': false }
          };
        });
        slotsList.forEach(slot => {
          const dateKey = slot.date;
          const timeKey = slot.start_time;
          let period = null;
          if (['09:00','10:00','11:00','12:00','13:00'].includes(timeKey)) period = 'morning';
          else if (['14:00','14:30','15:00','16:00','17:00'].includes(timeKey)) period = 'afternoon';
          else if (['18:00','18:30','19:00','19:30','20:00'].includes(timeKey)) period = 'evening';
          if (period && nestedAvailability[dateKey]) {
            nestedAvailability[dateKey][period][timeKey] = slot.is_available;
          }
        });
        this.availability = nestedAvailability;
        this.originalAvailability = JSON.parse(JSON.stringify(nestedAvailability));
      } catch (error) {
        console.error('Load failed:', error);
      }
    }
  }
}
</script>

<style scoped>
.doctor-availability-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
  padding: 1.5rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

.availability-card {
  max-width: 700px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  overflow: hidden;
}

.availability-header {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 1.5rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.doctor-avatar {
  width: 45px;
  height: 45px;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

h2 { margin: 0 0 0.25rem 0; font-size: 1.3rem; font-weight: 600; }
.availability-header p { margin: 0; opacity: 0.9; font-size: 0.9rem; }

.date-selection {
  padding: 1.5rem;
  background: #f8fafc;
}

.section-title {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 0.75rem;
}

.date-card {
  padding: 0.75rem 0.5rem;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
}

.date-card:hover:not(.active) {
  border-color: #10b981;
  transform: translateY(-1px);
}

.date-card.active {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.slots-section {
  padding: 1.5rem;
}

.current-date {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.current-date h4 {
  margin: 0;
  color: #10b981;
  font-size: 1.1rem;
  font-weight: 600;
}

.time-period {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border-radius: 12px;
  border-left: 4px solid;
}

.time-period.morning { background: #fef7e0; border-left-color: #f59e0b; }
.time-period.afternoon { background: #e0f2fe; border-left-color: #3b82f6; }
.time-period.evening { background: #fce7f3; border-left-color: #ec4899; }

.period-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-weight: 600;
}

.count {
  background: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
  gap: 0.75rem;
}

.slot-item {
  position: relative;
}

.slot-input {
  position: absolute;
  opacity: 0;
}

.slot-label {
  display: block;
  padding: 0.75rem 0.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
}

.slot-item.active .slot-label,
.slot-input:checked + .slot-label {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.summary-actions {
  padding: 1.5rem;
  border-top: 2px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.summary {
  font-weight: 600;
  color: #10b981;
  font-size: 1rem;
}

.buttons {
  display: flex;
  gap: 0.75rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn.save {
  background: #10b981;
  color: white;
}

.btn.reset {
  background: #6b7280;
  color: white;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #f1f5f9;
  color: #10b981;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  margin: 1rem auto;
  display: block;
  width: fit-content;
  border: 2px solid #e2e8f0;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

@media (max-width: 768px) {
  .date-grid { grid-template-columns: repeat(3, 1fr); }
  .slots-grid { grid-template-columns: repeat(3, 1fr); }
  .summary-actions { flex-direction: column; text-align: center; }
}
</style>
