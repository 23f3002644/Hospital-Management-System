<template>
<div class="departments-page">
    <!-- Your exact template unchanged -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div></div>
        <h2 style="text-align: center; margin-top: 1rem;">All Departments</h2>
        <RouterLink to="/add_department" class="btn btn-success">Add Department</RouterLink>
    </div>
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
            this.departments = res.data.departments;
        }).catch(err => this.error = err.response.data.message)
    }
 }
};
</script>

<style scoped>
.departments-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem 0;
    position: relative;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.departments-page::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(168,85,247,0.2) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(139,92,246,0.15) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
}

.container {
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(25px);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(139,92,246,0.3);
    margin: 2rem auto;
    max-width: 1200px;
    position: relative;
    overflow: hidden;
}

.container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #8b5cf6, #a78bfa, #c084fc, #8b5cf6);
    background-size: 300% 100%;
    animation: shimmer 4s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { background-position: 200% 0; }
    50% { background-position: -200% 0; }
}

.card {
    background: transparent;
    border: none;
    box-shadow: none;
}

.card-body {
    padding: 0;
}

h2 {
    color: #581c87 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c084fc 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center !important;
    margin: 0 0 1.5rem 0 !important;
    letter-spacing: -0.5px;
}

/* Replace your current .btn-success rules with these: */
.btn-success {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border: 2px solid rgba(16, 185, 129, 0.4) !important;
    color: white !important;
    padding: 1rem 2.5rem !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35) !important;
    text-decoration: none !important;
}

.btn-success:hover {
    background: linear-gradient(135deg, #059669, #047857) !important;
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 20px 40px rgba(16, 185, 129, 0.45) !important;
    color: white !important;
}


.table {
    margin-bottom: 0;
    border-radius: 16px;
    overflow: hidden;
}

.table th {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
    color: white !important;
    padding: 1.5rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    border: none !important;
    position: relative;
}

.table th::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #a78bfa, #c084fc);
}

.table td {
    padding: 1.75rem 1.5rem !important;
    border-bottom: 2px solid rgba(139,92,246,0.15) !important;
    color: #581c87 !important;
    vertical-align: middle;
    font-weight: 500;
    transition: all 0.3s ease !important;
}

.table td p {
    margin: 0 !important;
    color: #6d28d9 !important;
    line-height: 1.7 !important;
    font-size: 1rem;
}

.table tbody tr {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-radius: 12px !important;
    margin: 0.25rem 0 !important;
    background: rgba(255,255,255,0.7) !important;
}

.table tbody tr:hover {
    background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(168,85,247,0.1)) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 40px rgba(139,92,246,0.2) !important;
}

.table-bordered th,
.table-bordered td {
    border: 1px solid rgba(139,92,246,0.15) !important;
}

.text-center {
    color: #8b5cf6 !important;
    font-style: italic !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    padding: 2rem !important;
}

@media (max-width: 768px) {
    .departments-page {
        padding: 1rem 0;
    }
    
    .container {
        margin: 1rem !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
    }
    
    h2 {
        font-size: 2rem !important;
    }
    
    .table th,
    .table td {
        padding: 1rem 0.75rem !important;
        font-size: 0.95rem !important;
    }
    
    .btn-success {
        padding: 0.875rem 2rem !important;
        font-size: 1rem !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .d-flex {
        flex-direction: column !important;
        gap: 1rem !important;
    }
}
</style>
