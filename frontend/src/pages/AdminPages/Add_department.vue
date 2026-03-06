<template>
<div class="add-department-page">
    <div class="page-header">
        <div class="header-content">
            <div>
                <h2>Add New Department</h2>
            </div>
            <RouterLink to="/all_departments" class="back-btn">
                <i class="bi bi-arrow-left"></i> Back to Departments
            </RouterLink>
        </div>
    </div>
    
    <div class="department-form-card">
        <form @submit.prevent="addDepartment" class="department-form">
            <!-- Department Name -->
            <div class="form-group full-width">
                <label>Department Name</label>
                <input type="text" v-model="formData.name" required placeholder="e.g., Cardiology, Neurology">
            </div>

            <!-- Overview -->
            <div class="form-group full-width">
                <label>Overview</label>
                <textarea v-model="formData.overview" rows="5" required 
                    placeholder="Describe department services, specialties, and facilities..."></textarea>
            </div>

            <!-- Buttons -->
            <div class="form-actions">
                <button type="submit" class="btn-submit">
                    <i class="bi bi-hospital"></i> Add Department
                </button>
                <RouterLink to="/all_departments" class="btn-cancel">
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
                name: '',
                overview: '',
            },
            token: "",
            user_type: "",
            error: ""
        }
    },
    mounted() {
        this.tokenload();
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        addDepartment() {
            axios.post(`http://127.0.0.1:5000/api/new_department`, this.formData, {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.$router.push('/all_departments');
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to add department';
                console.error(this.error);
            });
        }
    }
}
</script>

<style scoped>
.add-department-page {
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

.department-form-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(139,92,246,0.25);
    max-width: 700px;
    margin: 0 auto;
}

.department-form-card::before {
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

.department-form {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    width: 100%;
}

.form-group label {
    color: #581c87;
    font-weight: 600;
    margin-bottom: 0.75rem;
    font-size: 1rem;
}

.form-group input,
.form-group textarea {
    padding: 1.25rem 1.5rem;
    border: 2px solid rgba(139,92,246,0.2);
    border-radius: 16px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.9);
    resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
    transform: translateY(-2px);
}

.form-group textarea {
    min-height: 120px;
    font-family: inherit;
}

.form-actions {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 1.5rem;
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
    transform: translateY(-3px) scale(1.02);
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
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px rgba(239,68,68,0.4);
    color: white;
}

@media (max-width: 768px) {
    .add-department-page {
        padding: 1rem;
    }
    
    .department-form-card {
        padding: 2rem 1.5rem;
        margin: 1rem;
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
