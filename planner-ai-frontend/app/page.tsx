"use client";

import { useState } from "react";
import CalendarPage from "@/components/calendar/MainCalendar";
import LoginLayout from "@/components/authenticate/login/LoginLayout";
import RegisterLayout from "@/components/authenticate/register/RegisterLayout";
import "@/styles/authenticate.css";

type View = "login" | "register" | "app";

export default function Home() {
  const [view, setView] = useState<View>("login");

  return (
    <>
      {view === "login" && (
        <LoginLayout
          onLogin={() => setView("app")}
          onRegister={() => setView("register")} // 👈 ASTA E CHEIA
        />
      )}

      {view === "register" && (
  <RegisterLayout
    onRegisterSuccess={() => setView("app")}
    onGoToLogin={() => setView("login")}
  />
)}


      {view === "app" && <CalendarPage />}
    </>
  );
}
