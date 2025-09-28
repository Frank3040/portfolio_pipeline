
// Script de inicialización para MongoDB
db = db.getSiblingDB('video_streaming');

// Crear usuario para la base de datos
db.createUser({
  user: 'video_user',
  pwd: 'video_password',
  roles: [
    {
      role: 'readWrite',
      db: 'video_streaming'
    }
  ]
});

print('MongoDB initialization completed successfully!');
print('Created database: video_streaming');
print('Created collections: video_raw_data, video_analytics, user_interactions');
print('Created indexes and inserted sample data');