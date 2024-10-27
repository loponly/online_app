import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ProjectScreen from './screens/ProjectScreen';
import AttendanceScreen from './screens/AttendanceScreen';
import LoginScreen from './screens/LoginScreen';
import { API_URL } from '@env'; // Use environment variable
import axios from 'axios';

const Stack = createStackNavigator();

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
    },
});

function App() {
    console.log('API URL:', API_URL); // Log the API URL for debugging
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <NavigationContainer>
                <Stack.Navigator initialRouteName="Login">
                    <Stack.Screen name="Login" component={LoginScreen} />
                    <Stack.Screen name="Project" component={ProjectScreen} />
                    <Stack.Screen name="Attendance" component={AttendanceScreen} />
                </Stack.Navigator>
            </NavigationContainer>
        </ThemeProvider>
    );
}

export default App;

// Function to join a project
export const joinProject = async (projectId, studentId) => {
    try {
        const response = await axios.post(`${API_URL}/join_project`, {
            project_id: projectId,
            student_id: studentId
        });
        console.log(response.data.message);
    } catch (error) {
        console.error('Error joining project:', error);
    }
};

// Function to submit feedback
export const submitFeedback = async (projectId, userId, content) => {
    try {
        const response = await axios.post(`${API_URL}/submit_feedback`, {
            project_id: projectId,
            user_id: userId,
            content: content
        });
        console.log(response.data.message);
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
};

// Function to view attendance
export const viewAttendance = async (userId) => {
    try {
        const response = await axios.get(`${API_URL}/view_attendance?user_id=${userId}`);
        console.log(response.data.attendance);
    } catch (error) {
        console.error('Error viewing attendance:', error);
    }
};
