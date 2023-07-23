import subprocess
from fastapi import APIRouter, HTTPException
from .. import schemas

router = APIRouter(
    tags=["Code Handler"],
    prefix="/code",
)


@router.post("/compare")
async def compare_code(request: schemas.LiveCode):
    inputs = request.input_.split("\n")
    expected_outputs = request.output.split("\n")
    starter_code = request.code

    try:
        test_cases_passed = 0
        for input_, expected_output in zip(inputs, expected_outputs):
            formatted_code = starter_code.format(input_)
            with open("code.pas", "w") as file:
                file.write(formatted_code)

            # Run the Pascal compiler and execute the compiled program, capturing its output
            subprocess.run(["fpc", "code.pas"])
            result = subprocess.run(
                ["./code"], input=input_, capture_output=True, text=True)

            final_result = result.stdout.strip()
            print(final_result)

            if final_result == expected_output:
                test_cases_passed += 1
            else:
                break

        if test_cases_passed == len(inputs):
            return {
                "message": "All test cases passed!",
                "status": "success",
                "stdout": final_result,
                "stderr": result.stderr.strip(),
                "stdin": input_,
            }
        else:
            return {
                "message": "Some test cases failed!",
                "status": "failure",
                "stdin": input_,
                "stdout": final_result,
                "stderr": result.stderr.strip(),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
