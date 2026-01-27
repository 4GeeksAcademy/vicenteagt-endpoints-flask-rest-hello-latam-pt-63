"""
Script para crear los ENUMs necesarios en PostgreSQL.
Ejecutar ANTES de pipenv run migrate
"""

import os
import sys

def setup_enums():
    print("🔧 Configurando ENUMs de PostgreSQL...")
    print("=" * 50)
    
    # Importar aquí para evitar errores de importación temprana
    from app import app, db
    
    with app.app_context():
        try:
            # SOLO type_media_enum por ahora
            sql = """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'type_media_enum') THEN
                    CREATE TYPE type_media_enum AS ENUM ('IMG', 'VIDEO');
                    RAISE NOTICE '✅ Tipo type_media_enum creado';
                ELSE
                    RAISE NOTICE '⚠️ Tipo type_media_enum ya existe';
                END IF;
            END $$;
            """
            
            db.engine.execute(sql)
            print("📦 type_media_enum: ['IMG', 'VIDEO']")
            print("   ✅ Configurado o ya existía")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:200]}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup de ENUMs completado")
    print("\n📝 Ahora puedes ejecutar:")
    print("   pipenv run migrate")
    print("   pipenv run upgrade")
    return True

if __name__ == '__main__':
    # Verificar que DATABASE_URL esté configurada
    if not os.environ.get('DATABASE_URL'):
        print("❌ Error: DATABASE_URL no está en .env")
        print("   Asegúrate de tener:")
        print("   DATABASE_URL=postgresql://usuario:password@localhost/basedatos")
        sys.exit(1)
    
    try:
        success = setup_enums()
        sys.exit(0 if success else 1)
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Ejecuta desde la raíz del proyecto")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)