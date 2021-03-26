#include <foxi/onnxifi_loader.h>

#include <stdio.h>

int main() {
    struct onnxifi_library *core = NULL;
    int ret = onnxifi_load(ONNXIFI_LOADER_FLAG_VERSION_1_0, NULL, core);
    if (!ret) {
        printf("Cannot load onnxifi lib\n");
        return 0;
    }
    onnxifi_unload(core);
    return 0;
}
