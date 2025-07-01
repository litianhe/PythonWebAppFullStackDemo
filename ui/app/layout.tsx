"use client";

import * as React from "react";
import "./globals.css";
import Header from "./components/Header";
import { useEffect, useState } from "react";
import { UserProvider } from "./context/UserContext";

type User = {
  username: string;
  email: string;
};

export default function LayoutClient({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");
        const headers: Record<string, string> = {};
        if (token) {
          headers["Authorization"] = `Bearer ${token}`;
        }
        
        const response = await fetch("/api/v1/user/me", {
          headers: new Headers(headers)
        });
        if (response.ok) {
          const data = await response.json();
          setUser({ username: data.username, email: data.email });
        }
      } catch (error) {
        console.error("Failed to fetch user", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <UserProvider user={user}>
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </UserProvider>
  );
}
