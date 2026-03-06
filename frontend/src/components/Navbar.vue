<template>
    <nav class="navbar navbar-expand-lg bg-info" v-if="token">
                <div class="container-fluid">
                    <h4>Welcome {{ this.name }}</h4>    
                    <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='admin'">

                        <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/dashboard">Home</RouterLink>
                            </li>
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/upcoming_appointments">Upcoming Appointment</RouterLink>
                            </li>
                            
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/registered_patients">Registered Patient</RouterLink>
                            </li>    
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/registered_doctors">Registered Doctor</RouterLink>
                            </li> 
                             <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/all_departments">All Departments</RouterLink>
                            </li>
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <RouterLink class="nav-link active" aria-current="page" to="/all_treatments">All Treatments</RouterLink>
                            </li>
                            <li class="nav-item list-group-item list-group-item-blue-violet">
                                <button @click="logout" class="btn btn-danger">Logout</button>
                            </li>
                            </ul>    
                            
                            
                        </div>
                        <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='doctor'">

                            <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" to="/doctor_dash">Home</RouterLink>
                                </li>
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" :to="`/availability_slot/${id}`">Availability Slot</RouterLink>
                                </li>
                                
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <button @click="logout" class="btn btn-danger">Logout</button>
                                </li>
                            </ul>    
                        </div>
                        <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='patient'">

                            <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" to="/patient_dash">Home</RouterLink>
                                </li>
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" :to="`/patient/history/${id}`">Past Appointment</RouterLink>
                                </li>
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" to="/search_doctor">Search Doctor</RouterLink>
                                </li>
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <RouterLink class="nav-link active" aria-current="page" :to="`/patient/update/${id}`">Update Profile</RouterLink>
                                </li>
                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                <button @click="download(id)" class="btn btn-secondary" :disabled="IsExporting">
                                {{ IsExporting ? '⏳ Generating...' : 'Download Treatments' }}</button>
                                </li>

                                <li class="nav-item list-group-item list-group-item-blue-violet">
                                    <button @click="logout" class="btn btn-danger">Logout</button>
                                </li>
                            </ul>    
                        </div>

                </div>
            </nav>
</template>

<script>
import axios from 'axios';

export default{
  data(){
    return{
      token:"",
      user_type:"",
      name:"",
      id:"",
      task_id: null,
      status:"",
      IsExporting: false,
      downloadUrl: null
    }
  },
  mounted() {
        this.loadToken()
  },
  created() {
    this.loadToken();  // Initial load
  },
  watch: {
    $route(to, from) {
      this.loadToken(); 
    }}, // Refresh on route change
  methods: {
    logout(){
        localStorage.clear();
        this.token = '';      // Reset reactive token
        this.user_type = '';  // Reset user_type
        this.name = '';
        this.id = '';
        this.$router.push('/')
    },
    loadToken() {
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }

            const user_type = localStorage.getItem('user_type');
            if(user_type){
                this.user_type = user_type
            }
            const name = localStorage.getItem('name');
            if(name){
                this.name = name
            }
            const id = localStorage.getItem('id');
            if(id){
                this.id = id
            }
            
        },
    async download(id) {
      this.IsExporting = true;
      try {
        const response = await axios.get(`http://localhost:5000/export_csv/${id}`);
        this.task_id = response.data.task_id;
        await this.pollStatus();
      } catch (error) {
        console.error('Export failed:', error);
        alert('❌ Export failed');
      } finally {
        this.IsExporting = false;
      }
    },

    async pollStatus() {
      const maxAttempts = 60; // 1min timeout
      let attempts = 0;

      while (attempts < maxAttempts) {
        try {
          // Use head request first to check status without downloading
          const statusRes = await axios.get(`http://localhost:5000/api/csv_result/${this.task_id}`);
          
          if (statusRes.status === 200) {
            // File is ready - trigger download in new tab
            // console.log("Task completed 1")
            window.open(`http://localhost:5000/api/csv_result/${this.task_id}`, '_blank');
            // console.log("Task completed 2")
            alert('✅ CSV ready for download!');
            // console.log("Task completed 3")
            return statusRes.result;
            
          }
        } catch (error) {
          // If HEAD fails but file might be ready, try direct access
          if (error.response?.status === 200) {
            window.open(`http://localhost:5000/api/csv_result/${this.task_id}`, '_blank');
            alert('✅ CSV ready for download!');
            return;
          }
          
          // Parse JSON status responses only
          if (error.response?.data?.status) {
            this.status = error.response.data.status;
            if (error.response.data.status === 'FAILURE') {
              alert('❌ Task failed');
              return;
            }
          }
        }

        // Still polling
        await new Promise(resolve => setTimeout(resolve, 2000));
        attempts++;
      }
      
      alert('⏰ Export timed out (60s)');
    }
  
     
  }
}
</script>

<style>
.navbar {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 50%, #a855f7 100%) !important;
    box-shadow: 0 4px 20px rgba(30, 64, 175, 0.3);
}

.list-group-item-blue-violet {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(124, 58, 237, 0.2) !important;
    color: #1e293b !important;
    transition: all 0.3s ease;
    margin: 0 2px;
    border-radius: 10px;
}

.list-group-item-blue-violet:hover {
    background: linear-gradient(135deg, #1e40af, #7c3aed) !important;
    color: white !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
}

.nav-link {
    color: #1e293b !important;
    font-weight: 500;
}

.list-group-item-blue-violet:hover .nav-link {
    color: white !important;
}

.navbar h4 {
    color: white !important;
    font-weight: 600;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
