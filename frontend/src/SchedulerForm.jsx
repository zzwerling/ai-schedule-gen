import React, { useState } from 'react';

const timeOptions = Array.from({ length: 48 }, (_, i) => {
    const hour24 = Math.floor(i / 2);
    const minutes = i % 2 === 0 ? '00' : '30';

    const period = hour24 < 12 ? 'AM' : 'PM';
    const hour12 = hour24 % 12 === 0 ? 12 : hour24 % 12;

    return `${hour12.toString().padStart(2, '0')}:${minutes} ${period}`;
});

export default function SchedulerForm() {
    const [sleepTime, setSleepTime] = useState('');
    const [wakeTime, setWakeTime] = useState('');
    const [fixedTasks, setFixedTasks] = useState([]);
    const [unfixedTasks, setUnfixedTasks] = useState([
        { name: '', duration: '' },
    ]);

    const [schedule, setSchedule] = useState(null);

    // --- Fixed Task Functions ---
    const addFixedTask = () => {
        setFixedTasks([...fixedTasks, { name: '', time: '' }]);
    };

    const updateFixedTask = (index, key, value) => {
        const updated = [...fixedTasks];
        updated[index][key] = value;
        setFixedTasks(updated);
    };

    // --- Unfixed Task Functions ---
    const addUnfixedTask = () => {
        setUnfixedTasks([...unfixedTasks, { name: '', duration: '' }]);
    };

    const updateUnfixedTask = (index, key, value) => {
        const updated = [...unfixedTasks];
        updated[index][key] = value;
        setUnfixedTasks(updated);
    };

    // --- Submission ---
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = {
            sleepTime,
            wakeTime,
            fixedTasks: fixedTasks.filter((t) => t.name && t.time),
            unfixedTasks: unfixedTasks.filter((t) => t.name && t.duration),
        };
        console.log('Form submitted:', data);

        try {
            const res = await fetch('http://localhost:8000/schedule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(data),
            });
            if (!res.ok) throw new Error('API Call Failed');
            const result = await res.json();
            console.log('Schedule received: ', result);
            const rawHTML = result.schedule
                .replace(/^```html\s*/i, '')   // strip starting ```html
                .replace(/```$/i, '');         // strip ending ```

            setSchedule(rawHTML);
        } catch (err) {
            console.error('Error calling API:', err);
            alert('An error occurred. Please try again later.')
        }

    };

    return (
        <div className="space-y-6 max-w-lg mx-auto p-6">
            <form onSubmit={handleSubmit} className="space-y-6 max-w-lg mx-auto p-6">
                {/* Sleep / Wake Time */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block font-bold mb-1">Wake Time</label>
                        <select
                            value={wakeTime}
                            onChange={(e) => setWakeTime(e.target.value)}
                            className="w-full border p-2 rounded"
                        >
                            <option value="">-- Select --</option>
                            {timeOptions.map((t) => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block font-bold mb-1">Sleep Time</label>
                        <select
                            value={sleepTime}
                            onChange={(e) => setSleepTime(e.target.value)}
                            className="w-full border p-2 rounded"
                        >
                            <option value="">-- Select --</option>
                            {timeOptions.map((t) => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>


                </div>

                {/* Fixed Tasks (Optional) */}
                <div>
                    <div className="flex justify-between items-center mb-2">
                        <label className="font-bold">Fixed Tasks (optional)</label>
                        <button
                            type="button"
                            onClick={addFixedTask}
                            className="text-blue-600 hover:underline text-sm"
                        >
                            + Add Task
                        </button>
                    </div>
                    {fixedTasks.map((task, i) => (
                        <div key={i} className="flex gap-2 mb-2">
                            <input
                                type="text"
                                placeholder="Task name"
                                value={task.name}
                                onChange={(e) => updateFixedTask(i, 'name', e.target.value)}
                                className="flex-1 border p-2 rounded"
                            />
                            <select
                                value={task.time}
                                onChange={(e) => updateFixedTask(i, 'time', e.target.value)}
                                className="border p-2 rounded"
                            >
                                <option value="">Time</option>
                                {timeOptions.map((t) => (
                                    <option key={t} value={t}>{t}</option>
                                ))}
                            </select>
                        </div>
                    ))}
                </div>

                {/* Unfixed Tasks (Required) */}
                <div>
                    <div className="flex justify-between items-center mb-2">
                        <label className="font-bold">Unfixed Tasks (required)</label>
                        <button
                            type="button"
                            onClick={addUnfixedTask}
                            className="text-blue-600 hover:underline text-sm"
                        >
                            + Add Task
                        </button>
                    </div>
                    {unfixedTasks.map((task, i) => (
                        <div key={i} className="flex gap-2 mb-2">
                            <input
                                type="text"
                                placeholder="Task name"
                                value={task.name}
                                onChange={(e) => updateUnfixedTask(i, 'name', e.target.value)}
                                className="flex-1 border p-2 rounded"
                                required
                            />
                            <input
                                type="number"
                                placeholder="Duration (min)"
                                value={task.duration}
                                onChange={(e) => updateUnfixedTask(i, 'duration', e.target.value)}
                                className="w-36 border p-2 rounded"
                                required
                            />
                        </div>
                    ))}
                </div>

                {/* Submit */}
                <button
                    type="submit"
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                >
                    Generate Schedule
                </button>
            </form>


            {schedule && (
                <div
                    className="mt-8 p-4 bg-white border rounded shadow"
                    dangerouslySetInnerHTML={{ __html: schedule}}
                />
            )}


        </div>

    );
}

