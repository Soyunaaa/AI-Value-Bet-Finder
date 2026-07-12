import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Analysis from "./pages/Analysis";
import Dashboard from "./pages/Dashboard";
import Live from "./pages/Live";
import Statistics from "./pages/Statistics";
import ValueBets from "./pages/ValueBets";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />

        <Route
          path="/live"
          element={<Live />}
        />

        <Route
          path="/value-bets"
          element={<ValueBets />}
        />

        <Route
          path="/analysis/:id"
          element={<Analysis />}
        />

        <Route
          path="/statistics"
          element={<Statistics />}
        />

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}