"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useUser } from "../context/UserContext";

export default function Header() {
  const { user } = useUser();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await fetch("/api/v1/auth/logout", {
        method: "POST",
      });
      localStorage.removeItem("access_token");
      sessionStorage.removeItem("access_token");
      router.refresh();
      router.push("/");
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <Link href="/" className="text-xl font-bold text-indigo-600">
          Comment System
        </Link>

        <div className="flex items-center space-x-4">
          {user?.username? (
            <>
              <div className="hidden sm:block">
                <p className="text-sm font-medium">{user.username}</p>
                <p className="text-xs text-gray-500">{user.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
