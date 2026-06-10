import { useState } from "react";

import styles from "../styles/AuthForm.module.css";

interface AuthFormProps {
  onLogin: (username: string, password: string) => void;
  onRegister: (username: string, password: string) => void;
  error: string | null;
}

function AuthForm({ onLogin, onRegister, error }: AuthFormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <form className={styles.form} onSubmit={(e) => e.preventDefault()}>
      <input
        className={styles.input}
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        autoComplete="username"
      />
      <input
        className={styles.input}
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        autoComplete="current-password"
      />
      <div className={styles.actions}>
        <button
          type="submit"
          className={styles.button}
          onClick={() => onLogin(username, password)}
        >
          Log in
        </button>
        <button
          type="button"
          className={styles.button}
          onClick={() => onRegister(username, password)}
        >
          Register
        </button>
      </div>
      {error && <p className={styles.error}>{error}</p>}
    </form>
  );
}

export default AuthForm;
