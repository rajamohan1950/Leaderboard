import { useEffect, useState } from "react";

export default function Leaderboard() {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    fetch("https://your-api-url.com/top/10")
      .then(res => res.json())
      .then(data => setScores(data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Leaderboard</h1>
      <ul className="mt-4">
        {scores.map((s, i) => (
          <li key={i} className="text-lg">{s.user}: {s.score}</li>
        ))}
      </ul>
    </div>
  );
}

