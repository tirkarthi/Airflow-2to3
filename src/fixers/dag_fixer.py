import libcst as cst
from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor


class DagFixerCommand(VisitorBasedCodemodCommand):
    """
    Fixes deprecation warning and removals related to DAG construction.

    replacements includes a dictionary of old and updated names.
    removals includes a list of names removed.
    updates includes a dictionary of old and updated values for a given parameter
    """

    DESCRIPTION = "Fixes deprecation warning and removals related to DAG construction."

    replacements = {
        "schedule_interval": "schedule",
        "timetable": "schedule",
        "concurrency": "max_active_tasks",
    }

    removals = ["full_filepath"]

    updates = {"default_view": ("tree", '"grid"')}

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if isinstance(original_node.func, cst.Name) and original_node.func.value in (
            "DAG",
            "dag",
        ):
            original_args = list(original_node.args)
            updated_args = []

            for index, arg in enumerate(original_args):
                if arg.keyword and arg.keyword.value in self.replacements:
                    updated_args.append(
                        arg.with_changes(
                            keyword=arg.keyword.with_changes(
                                value=self.replacements.get(arg.keyword.value)
                            )
                        )
                    )
                elif (
                    arg.keyword
                    and arg.keyword.value in self.updates
                    and arg.value.raw_value == self.updates.get(arg.keyword.value)[0]
                ):
                    updated_args.append(
                        arg.with_changes(
                            value=arg.value.with_changes(
                                value=self.updates.get(arg.keyword.value)[1]
                            )
                        )
                    )
                elif arg.keyword and arg.keyword.value in self.removals:
                    continue
                else:
                    updated_args.append(arg)

            return updated_node.with_changes(args=tuple(updated_args))

        return updated_node
