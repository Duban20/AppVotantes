from django.db import migrations

def migrate_lider_asignado_to_lider_eg(apps, schema_editor):
    Votante = apps.get_model('appformulario', 'Votante')
    LiderEG = apps.get_model('appformulario', 'LiderEG')

    # 1. Crear LiderEG para cada líder antiguo
    lideres = {}

    for lider in Votante.objects.filter(rol='LIDER_VOTANTE'):
        lider_eg, _ = LiderEG.objects.get_or_create(
            votante=lider
        )
        lideres[lider.id] = lider_eg

    # 2. Migrar la FK: Votante.lider_asignado -> Votante.lider_eg
    votantes = Votante.objects.exclude(lider_asignado__isnull=True)

    for votante in votantes:
        lider_antiguo = votante.lider_asignado
        lider_eg = lideres.get(lider_antiguo.id)

        if lider_eg:
            votante.lider_eg = lider_eg
            votante.save(update_fields=['lider_eg'])

class Migration(migrations.Migration):

    dependencies = [
        ('appformulario', '0010_alter_historicalvotante_rol_alter_votante_rol_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_lider_asignado_to_lider_eg),
    ]
