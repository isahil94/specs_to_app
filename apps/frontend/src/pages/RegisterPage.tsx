import { Link } from 'react-router-dom';
import './AuthPage.css';

export function RegisterPage() {
  return (
    <main className="auth-page" aria-labelledby="register-heading">
      <section className="auth-panel">
        <h1 id="register-heading">Create your account</h1>
        <form className="auth-form">
          <label htmlFor="displayName">Display name</label>
          <input id="displayName" name="displayName" type="text" required placeholder="Your name" />

          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" required placeholder="you@example.com" />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" required placeholder="Create a password" />

          <button type="submit" className="button primary">Register</button>
          <p className="auth-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
