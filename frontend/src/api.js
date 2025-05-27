import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const createTask = async (userId, data) => {
  const response = await axios.post(`${API_URL}/tasks/`, {
    user_id: userId,
    data
  });
  return response.data;
};

export const getTaskStatus = async (taskId) => {
  const response = await axios.get(`${API_URL}/tasks/${taskId}/`);
  return response.data;
};
