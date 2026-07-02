import './ProfilePage.css';

export function ProfilePage() {
  return (
    <section className="page profile-page" aria-labelledby="profile-heading">
      <div className="page-header">
        <div>
          <p className="eyebrow">Profile</p>
          <h1 id="profile-heading">Your profile</h1>
        </div>
      </div>
      <div className="profile-card">
        <div className="profile-row">
          <span className="profile-label">Display name</span>
          <span>Alex Morgan</span>
        </div>
        <div className="profile-row">
          <span className="profile-label">Email</span>
          <span>alex@example.com</span>
        </div>
        <div className="profile-row">
          <span className="profile-label">Teams</span>
          <span>Design, Product</span>
        </div>
      </div>
    </section>
  );
}
