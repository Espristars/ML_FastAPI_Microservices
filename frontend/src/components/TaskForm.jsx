import React, { useState } from 'react';
import { createTask, getTaskStatus } from '../api';

const TaskForm = ({ userId }) => {
  const [inputData, setInputData] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const task = await createTask(userId, inputData);
    setTaskId(task.id);
    setStatus('pending');
    setResult(null);
  };

  const checkStatus = async () => {
    if (!taskId) return;
    const task = await getTaskStatus(taskId);
    setStatus(task.status);
    if (task.status === 'completed') {
      setResult(task.result);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder="Введите данные задачи"
        />
        <button type="submit">Отправить</button>
      </form>
      {taskId && (
        <div>
          <p>Статус: {status}</p>
          {status !== 'completed' && (
            <button onClick={checkStatus}>Проверить статус</button>
          )}
          {result && (
            <div>
              <h3>Результат:</h3>
              <pre>{result}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TaskForm;
