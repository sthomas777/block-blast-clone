import styles from "../styles/UserBar.module.css";

interface UserBarProps {
  username: string;
  onLogout: () => void;
}

function UserBar({ username, onLogout }: UserBarProps) {
  return (
    <div className={styles.bar}>
      <span className={styles.greeting}>
        Signed in as <strong>{username}</strong>
      </span>
      <button className={styles.logout} onClick={onLogout}>
        Log out
      </button>
    </div>
  );
}

export default UserBar;
