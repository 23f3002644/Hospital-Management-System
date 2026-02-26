<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-lg">
          <div class="card-header bg-primary text-white text-center">
            <h3>Book Appointment</h3>
            <p class="mb-0">Doctor: {{ doc_name }}</p>
          </div>
          <div class="card-body p-4">
            
            <!-- ERROR DISPLAY -->
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            
            <!-- LOADING -->
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary"></div>
              <p class="mt-2">Loading available slots...</p>
            </div>

            <!-- DATE PICKER -->
            <div v-else class="mb-4">
              <label class="form-label fw-bold">Select Date <span class="text-danger">*</span></label>
              <input 
                type="date" 
                class="form-control form-control-lg" 
                v-model="selectedDate"
                :min="minDate"
                @change="loadAvailableSlots"
                required
              >
            </div>

            <!-- AVAILABLE SLOTS (Backend-Driven) -->
            <div v-if="selectedDate && !loading" class="time-slots-section">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <label class="form-label fw-bold mb-0">Available Slots ({{ availableSlots.length }})</label>
                <span v-if="availableSlots.length === 0" class="badge bg-warning">No slots available</span>
              </div>

              <!-- MORNING SLOTS -->
              <div v-if="morningAvailableSlots.length" class="row mb-4">
                <div class="col-md-4">
                  <h6 class="text-muted">🕐 Morning</h6>
                </div>
                <div class="col-md-8">
                  <div class="btn-group w-100" role="group">
                    <button 
                      v-for="slot in morningAvailableSlots" :key="slot.start_time"
                      class="btn btn-outline-success me-1 mb-1 time-btn"
                      :class="{ 'btn-success text-white': selectedSlot === slot.start_time }"
                      @click="selectSlot(slot.start_time)">{{ formatTime(slot.start_time) }}</button>
                  </div>
                </div>
              </div>

              <!-- AFTERNOON SLOTS -->
              <div v-if="afternoonAvailableSlots.length" class="row mb-4">
                <div class="col-md-4">
                  <h6 class="text-muted">🌞 Afternoon</h6>
                </div>
                <div class="col-md-8">
                  <div class="btn-group w-100" role="group">
                    <button 
                      v-for="slot in afternoonAvailableSlots" :key="slot.start_time"
                      class="btn btn-outline-success me-1 mb-1 time-btn"
                      :class="{ 'btn-success text-white': selectedSlot === slot.start_time }"
                      @click="selectSlot(slot.start_time)"
                    >{{ formatTime(slot.start_time) }}</button>
                  </div>
                </div>
              </div>

              <!-- EVENING SLOTS -->
              <div v-if="eveningAvailableSlots.length" class="row mb-4">
                <div class="col-md-4">
                  <h6 class="text-muted">🌙 Evening</h6>
                </div>
                <div class="col-md-8">
                  <div class="btn-group w-100" role="group">
                    <button 
                      v-for="slot in eveningAvailableSlots" :key="slot.start_time"
                      class="btn btn-outline-success me-1 mb-1 time-btn"
                      :class="{ 'btn-success text-white': selectedSlot === slot.start_time }"
                      @click="selectSlot(slot.start_time)" >{{ formatTime(slot.start_time) }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- NO SLOTS MESSAGE -->
              <div v-if="availableSlots.length === 0" class="text-center py-5">
                <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">No available slots for {{ selectedDate }}</h5>
                <p class="text-muted">Please try another date</p>
              </div>

              <!-- SUMMARY & BOOK -->
              <div v-if="selectedSlot" class="row mt-4">
                <div class="col-12 text-center">
                  <div class="alert alert-success">
                    <h5>✅ Your Selection:</h5>
                    <p class="mb-0">
                      <strong>{{ selectedDate }}</strong> at 
                      <strong>{{ formatTime(selectedSlot) }}</strong>
                    </p>
                    <small>Doctor: {{  doc_name }}</small>
                  </div>
                  <button class="btn btn-success btn-lg px-5" @click="bookAppointment">
                    <i class="fas fa-calendar-check"></i> Book Appointment
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-4">
          <RouterLink :to="`/department_details/${departmentId}`" class="btn btn-primary">
            ← Back to Department
          </RouterLink>
        </div>
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
      doc_name:"",
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
    doctorName() {
      return this.$route.params.doctor || 'Doctor';
    },
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
    // this.formData.doctor = this.$route.params.doctor || '';
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

    loadinfo(){
      //need to reset form data when doctor or department changes
            const doc_id = this.$route.params.doctor_id; // Assuming the route is defined with a parameter named 'name'
            const response = axios.get(`http://127.0.0.1:5000//api/doctor_details/${doc_id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            response
            .then(res => {
                    // Handle the response data as needed
                    this.formData.doctor = res.data.doctor.name; // Assuming the API returns a single doctor object
                    this.doc_name = res.data.doctor.name
                    this.dept_name = res.data.doctor.department_name; // Assuming the doctor object contains a department_name field
                    this.departmentId = res.data.dept_id; // Assuming the API returns the department ID
                    console.log(this.dept_id);
                    console.log(res.data.doctor.name)
            }).catch(err => this.error = err.response.data.message)
        //ended here


      this.formData.doctor = null;
      this.departmentId = null;

    },

    async loadAvailableSlots() {
      if (!this.selectedDate) return;
      
      this.loading = true;
      this.error = '';
      
      try {
        // Get doctor_id from route or lookup by name
        const doctorId = this.$route.params.doctor_id || 1; // Fallback to 1 if not provided
        const doctorResponse = await axios.get(
          `http://127.0.0.1:5000/api/doctor_available_slots/${doctorId}?date=${this.selectedDate}`,
          { headers: { 'Authentication-Token': this.token } }
        );
        
        this.availableSlots = doctorResponse.data.available_slots
          .filter(slot => slot.is_available)  // Only available slots
          .map(slot => ({
            start_time: slot.start_time,
            date: slot.date
          }));
        
        this.formData.date = this.selectedDate;
        this.selectedSlot = '';  // Reset selection
        
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
        const response = await axios.post(
          'http://127.0.0.1:5000/api/appointment',
          this.formData,
          {
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': this.token
            }
          }
        );
        
        alert('✅ Appointment booked successfully!');
        this.$router.push('/patient_dash');
      } catch (error) {
        this.error = error.response?.data?.message || 'Booking failed';
      }
    }
  },
  watch: {
    selectedDate(newVal) {
      if (newVal) {
        this.loadAvailableSlots();
      }
    }
  }
}
</script>

<style scoped>
.time-btn {
  min-width: 75px;
  border-radius: 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.time-btn:hover:not(.btn-success) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,123,255,0.3);
}

.btn-success {
  box-shadow: 0 4px 15px rgba(40,167,69,0.4) !important;
}

.card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
}
</style>
