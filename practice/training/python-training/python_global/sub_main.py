#Valid only for constants
import folder.main as main

print(f"_my_var: {main.__my_var}")

main.print_my_var()
main.init()
main.print_my_var()

print(f"_my_var (after init, before import): {main.__my_var}")
print(f"_my_var (after init, after import): {main.__my_var}")

main.print_my_var()