# TVM

Organization → Branch → Department → Position → Users → Tasks

Это прям супер-логично:
- Branch принадлежит Organization
- Department принадлежит Branch
- Position принадлежит Department
- User принадлежит Position (и косвенно отделу/филиалу)
- Task принадлежит User

То есть foreign key ставишь вниз по дереву.