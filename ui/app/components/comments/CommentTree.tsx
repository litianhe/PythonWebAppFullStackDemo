"use client";

import { useEffect, useState } from "react";
import CommentForm from "./CommentForm";

type User = {
  id: number;
  username: string;
  email: string;
};

type Comment = {
  id: number;
  content: string;
  created_at: string;
  user_id: number;
  user: User;
  parent_id: number;
  children: Comment[];
};

type CommentTreeProps = {
  user: {
    username: string;
    email: string;
  } | null;
};

export default function CommentTree({ user }: CommentTreeProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refreshComments = async () => {
    try {
      const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");
      const headers: Record<string, string> = {};
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch("/api/v1/comments/", {
        headers: new Headers(headers)
      });

      if (!response.ok) {
        throw new Error("Failed to fetch comments");
      }

      const data = await response.json();
      setComments(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch comments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshComments();
  }, []);


  const renderComment = (comment: Comment, depth = 0) => (
    <div
      key={comment.id}
      className={`relative group transition-all duration-200 ${
        depth === 0
          ? "mb-6"
          : "mb-4 ml-6 border-l-2 border-blue-100 pl-4"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-gray-800">{comment.user.username}</span>
            <span className="text-xs text-gray-400">
              {new Date(comment.created_at).toLocaleDateString()}&nbsp;
              {new Date(comment.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
          <p className="mt-1 text-gray-700 whitespace-pre-wrap text-base leading-relaxed">
            {comment.content}
          </p>
          <div className="mt-2">
            <CommentForm
              parentId={comment.id}
              onSuccess={refreshComments}
            />
          </div>
        </div>
      </div>
      {comment.children && comment.children.length > 0 && (
        <div className="mt-3">
          {comment.children.map(child => renderComment(child, depth + 1))}
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto px-2 py-8">
      {user && (
        <div className="mb-8 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow p-6">
          <h2 className="text-2xl font-bold mb-3 text-gray-800">Post a Comment</h2>
          <CommentForm onSuccess={refreshComments} />
        </div>
      )}

      <div className="bg-white rounded-xl shadow border border-blue-100 overflow-hidden">
        <div className="p-6">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-pulse flex space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
            </div>
          ) : error ? (
            <div className="py-8 text-center text-red-500">
              {error}
            </div>
          ) : comments.length > 0 ? (
            <div className="space-y-2">
              {comments.map(comment => renderComment(comment))}
            </div>
          ) : (
            <div className="py-12 text-center">
              <p className="text-gray-500 mb-4">No comments yet.</p>
              {!user && (
                <p className="text-sm text-gray-400">
                  Login to post a comment.
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}