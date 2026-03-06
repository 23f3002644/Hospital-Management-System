<template>
<div class="add-doctor-page">
    <div class="page-header">
        <div class="header-content">
            <div>
                <h2>Add New Doctor</h2>
            </div>
            <RouterLink to="/registered_doctors" class="back-btn">
                <i class="bi bi-arrow-left"></i> Back to Doctors
            </RouterLink>
        </div>
    </div>
    
    <div class="doctor-form-card">
        <form @submit.prevent="addDoctor" class="doctor-form">
            <!-- Email & Password -->
            <div class="form-row">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" v-model="formData.email" required>
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" v-model="formData.password" required>
                </div>
            </div>

            <!-- Name & Age -->
            <div class="form-row">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" v-model="formData.name" required>
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" v-model="formData.age" required>
                </div>
            </div>

            <!-- Contact & Address -->
            <div class="form-row">
                <div class="form-group">
                    <label>Contact Number</label>
                    <input type="number" v-model="formData.contact_number" required>
                </div>
                <div class="form-group">
                    <label>Address</label>
                    <input type="text" v-model="formData.address" required>
                </div>
            </div>

            <!-- Gender & Specialty -->
            <div class="form-row">
                <div class="form-group">
                    <label>Gender</label>
                    <select v-model="formData.gender" required>
                        <option value="" disabled selected>Select gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Specialty</label>
                    <input type="text" v-model="formData.specialty" required>
                </div>
            </div>

            <!-- Department & Description -->
            <div class="form-row">
                <div class="form-group full-width">
                    <label>Department</label>
                    <select v-model="formData.department_name" required>
                        <option value="" disabled selected>Select department</option>
                        <option v-for="department in departments" :key="department.id" :value="department.name">
                            {{ department.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="form-group full-width">
                <label>Description</label>
                <textarea v-model="formData.description" rows="4" required></textarea>
            </div>

            <!-- Buttons -->
            <div class="form-actions">
                <button type="submit" class="btn-submit">
                    <i class="bi bi-person-plus"></i> Add Doctor
                </button>
                <RouterLink to="/registered_doctors" class="btn-cancel">
                    Cancel
                </RouterLink>
            </div>
        </form>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            formData: {
                email: '',
                password: '',
                name: '',
                age: '',
                gender: '',
                specialty: '',
                department_name: '',
                description: '',
                address: '',
                contact_number: ''
            },
            token: "",
            user_type: "",
            departments: [],
            error: ""
        }
    },
    mounted() {
        this.tokenload();
        this.loadDepartment();
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        addDoctor() {
            axios.post(`http://127.0.0.1:5000/api/new_doctor`, this.formData, {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.$router.push('/registered_doctors');
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to add doctor';
                console.error(this.error);
            });
        },
        loadDepartment() {
            axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.departments = res.data.departments || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load departments';
                console.error(this.error);
            });
        }
    }
}
</script>

<style scoped>
.add-doctor-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.page-header {
    margin-bottom: 3rem;
    text-align: center;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.page-header h2 {
    color: #581c87;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-header p {
    color: #6b21a8;
    margin: 0.25rem 0 0 0;
    font-size: 1.1rem;
}

.back-btn {
    background: linear-gradient(135deg, #6b7280, #4b5563);
    color: white;
    padding: 0.875rem 1.5rem;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.back-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(107,114,128,0.4);
    color: white;
}

.doctor-form-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(139,92,246,0.25);
    max-width: 800px;
    margin: 0 auto;
}

.doctor-form-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #8b5cf6, #a78bfa, #c084fc);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    border-radius: 24px 24px 0 0;
}

@keyframes shimmer {
    0%, 100% { background-position: 200% 0; }
    50% { background-position: 0 0; }
}

.doctor-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    color: #581c87;
    font-weight: 600;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    padding: 1rem 1.25rem;
    border: 2px solid rgba(139,92,246,0.2);
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.9);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
    transform: translateY(-1px);
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1rem;
}

.btn-submit {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border: none;
    padding: 1.25rem 3rem;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.4s ease;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    box-shadow: 0 8px 25px rgba(16,185,129,0.3);
}

.btn-submit:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(16,185,129,0.4);
}

.btn-cancel {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    padding: 1.25rem 2.5rem;
    border-radius: 16px;
    text-decoration: none;
    font-weight: 700;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    transition: all 0.4s ease;
    box-shadow: 0 8px 25px rgba(239,68,68,0.3);
}

.btn-cancel:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(239,68,68,0.4);
    color: white;
}

@media (max-width: 768px) {
    .add-doctor-page {
        padding: 1rem;
    }
    
    .doctor-form-card {
        padding: 2rem 1.5rem;
        margin: 1rem;
    }
    
    .form-row {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .header-content {
        flex-direction: column;
        text-align: center;
    }
    
    .form-actions {
        flex-direction: column;
    }
    
    .btn-submit,
    .btn-cancel {
        width: 100%;
        justify-content: center;
    }
}
</style>
