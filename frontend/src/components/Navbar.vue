<template>
    <nav class="navbar navbar-expand-lg bg-info" v-if="token">
                <div class="container-fluid">
                    <h4>Welcome {{ this.name }}</h4>   
                    <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='admin'">

                        <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/dashboard">Home</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/upcoming_appointments">Upcoming Appointment</RouterLink>
                            </li>
                            
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/registered_patients">Registered Patient</RouterLink>
                            </li>   
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/registered_doctors">Registered Doctor</RouterLink>
                            </li> 
                             <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/all_departments">All Departments</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/all_treatments">All Treatments</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <button @click="logout" class="btn btn-danger">Logout</button>
                            </li>
                            </ul>   
                        
                        
                        

                    </div>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='doctor'">

                        <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/doctor_dash">Home</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" :to="`/availability_slot/${id}`">Availability Slot</RouterLink>
                            </li>
                             
                            <li class="nav-item list-group-item  list-group-item-success">
                                <button @click="logout" class="btn btn-danger">Logout</button>
                            </li>
                        </ul>   
                    </div>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_type=='patient'">

                        <ul class="navbar-nav mx-auto mb-2 mb-lg-0 list-group list-group-horizontal text-center">
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/patient_dash">Home</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" :to="`/patient/history/${id}`">Past Appointment</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" to="/search_doctor">Search Doctor</RouterLink>
                            </li>
                            <li class="nav-item list-group-item  list-group-item-success">
                                <RouterLink class="nav-link active" aria-current="page" :to="`/patient/update/${id}`">Update Profile</RouterLink>
                            </li>
                             
                            <li class="nav-item list-group-item  list-group-item-success">
                                <button @click="logout" class="btn btn-danger">Logout</button>
                            </li>
                        </ul>   
                    </div>

                </div>
            </nav>
</template>

<script>
export default{
  data(){
    return{
      token:"",
      user_type:"",
      name:"",
      id:""
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
            
        } 
  }

}
</script>


<style>
.navbar {
    background: linear-gradient(135deg, #075bd1 0%, #b374c5 100%) !important;
}

</style>