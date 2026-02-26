<template>
    <div>
        <h2>This is Department {{ this.dept_name }}</h2>
        <div>
            <h4>Overview</h4>
            {{ this.overview }}
        </div>
        <div class ="bottom-section">
                <div id ="content" class="overflow-auto">
                        <h3 class="heading" >Doctor's List</h3>
                        <div id="table1" class="border" style="max-height:150px;overflow-y: scroll;">
                        <table class="table table-striped table-bordered" >
                            <thead>
                                <tr>
                                    <th scope="col">Doctor Name</th>
                                    <th scope="col">Doctor Availibilty</th>
                                    <th scope="col">View Doctor</th>
                                    
                                </tr>
                            </thead>
                            <div v-if="doctors.length === 0" class="text-center p-3">
                                No Doctors.
                            </div>
                            <tbody v-else>
                                <tr v-for="doctor in doctors" :key="doctor.id">
                                    <td>{{ doctor.name }}</td>
                                    <td><RouterLink :to="{ name: 'Appointment', params: { department: this.dept_name, doctor_id: doctor.id } }"><button>Check Availibilty</button></RouterLink></td>
                                    <td> <RouterLink :to="{ name: 'Doctor_details', params: { id: doctor.id } }"><button>view details</button></RouterLink></td>

                                    
                                </tr>
                            </tbody>
                        </table>
                        </div>
                </div>
            </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "Department_details",
    data() {
        return {
            token:"",
            doctors: [],
            overview:"",
            dept_name:""
            // Data properties can be added here if needed
        };
    },
    mounted(){
        this.tokenload()
        this.department_details()

    }
    ,
    methods:{
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
         department_details(){
            const dept_id = this.$route.params.id; // Assuming the route is defined with a parameter named 'id'
            // this.dept_name = dept_id
            const response = axios.get(`http://127.0.0.1:5000/api/department_doctors/${dept_id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            response
            .then(res => {
                    this.doctors = res.data.doctors;
                    this.overview = res.data.department_views.overview;
                    this.dept_name = res.data.department_views.name;
                    
            }).catch(err => this.error = err.response.data.message)

        }
    }
}

</script>