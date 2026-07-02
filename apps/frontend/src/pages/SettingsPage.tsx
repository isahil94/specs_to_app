import './SettingsPage.css';

export function SettingsPage() {
  return (
    <section className="page settings-page" aria-labelledby="settings-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Settings</p>
          <h1 id="settings-heading">Preferences</h1>
        </div>
      </div>
      <form className="settings-form" aria-label="User settings">
        <label htmlFor="theme">Theme</label>
        <select id="theme" name="theme" defaultValue="system">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System</option>
        </select>

        <label htmlFor="language">Language</label>
        <select id="language" name="language" defaultValue="en">
          <option value="en">English</option>
          <option value="es">Español</option>
        </select>

        <label htmlFor="timeZone">Time zone</label>
        <input id="timeZone" name="timeZone" type="text" defaultValue="UTC" />

        <button type="submit" className="button primary">Save preferences</button>
      </form>
    </section>
  );
}
