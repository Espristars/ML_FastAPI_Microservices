import React from 'react';
import TaskForm from './components/TaskForm';

const App = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get('user_id') || 'default_user';

  return (
    <div>
      <h1>Task App</h1>
      <TaskForm userId={userId} />
    </div>
  );
};

export default App;
