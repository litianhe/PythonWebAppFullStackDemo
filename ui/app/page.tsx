"use client";

import { useState } from "react";
import CommentTree from "./components/comments/CommentTree";
import LoginForm from "./components/auth/LoginForm";
import RegisterForm from "./components/auth/RegisterForm";
import { useUser } from "./context/UserContext";

export default function Page() {
  const { user } = useUser();
  const [showRegister, setShowRegister] = useState(false);

  return (
    <div className="py-8">
      {!user && (
        <div className="max-w-md mx-auto">
          {showRegister ? (
            <>
              <RegisterForm />
              <p className="mt-4 text-center text-sm">
                Already have an account?{" "}
                <button
                  onClick={() => setShowRegister(false)}
                  className="text-indigo-600 hover:text-indigo-500 font-medium"
                >
                  Login
                </button>
              </p>
            </>
          ) : (
            <>
              <LoginForm />
              <p className="mt-4 text-center text-sm">
                Don't have an account?{" "}
                <button
                  onClick={() => setShowRegister(true)}
                  className="text-indigo-600 hover:text-indigo-500 font-medium"
                >
                  Register
                </button>
              </p>
            </>
          )}
        </div>
      )}

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Comments</h2>
        <CommentTree user={user} />
      </div>
    </div>
  );
}
