<template>
<div>
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div></div>
        <h2 style="text-align: center; margin-top: 1rem;">All Departments</h2>
        <RouterLink to="/add_department" class="btn btn-success">Add Department</RouterLink>
    </div>
    <!-- <h2 class="text-center mt-4">All Departments</h2> -->
    <!-- <h2 style="text-align: center;">Registered Departments</h2>
    <RouterLink to="/add_department" class="btn btn-success">Add Department</RouterLink> -->
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Department Name</th>
                                    <th>Overview</th>
                                </tr>
                            </thead>
                            <tbody v-if="departments.length === 0">
                                <tr>
                                    <td colspan="5" class="text-center">No departments found.</td>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr v-for="department in departments" :key="department.id">
                                    <td>{{ department.name }}</td>
                                    <td><p>{{ department.overview }}</p></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
        token: "",
        departments: [],
    };
  },
  mounted() {
    this.tokenload();
    this.loadDepartments();
  },
  methods: {
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
        loadDepartments(){
            const response = axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                }
            })
            response
            .then(res => {
                    // Handle the response data as needed
                    this.departments = res.data.departments;
            }).catch(err => this.error = err.response.data.message)
        
        }
    // fetchDepartments() {
    //   fetch("http://localhost:8000/api/departments")
    //     .then(response => response.json())
    //     .then(data => {
    //       this.departments = data;
    //       this.filteredDepartments = data;
    //     })
    //     .catch(error => console.error("Error fetching departments:", error));
    // },
    // deleteDepartment(id) {
    //   fetch(`http://localhost:8000/api/departments/${id}`, { method: "DELETE" })
    //     .then(() => this.fetchDepartments())
    //     .catch(error => console.error("Error deleting department:", error));
    // }
  }
};
</script>