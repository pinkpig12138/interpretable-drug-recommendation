results = []

for optimizer in optimizer_list:
    for hidden_layer_num in hidden_layer_num_list:
        for hidden_layer_units in hidden_layer_units_list:
            for batch_size in batch_size_list:
                for hidden_layer_dropout in hidden_layer_dropout_list:
                    for input_layer_dropout in input_layer_dropout_list:
                        for use_kernel_regularizer in use_kernel_regularizer_list:
                            if hidden_layer_dropout == True or input_layer_dropout == True:
                                for dropout_rate in dropout_rate_list:
                                    if use_kernel_regularizer == True:
                                        for kernel_regularizer in kernel_regularizer_list:
                                            print(
                                                "优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s，正则化：%s" % (
                                                optimizer, hidden_layer_num, hidden_layer_units, batch_size,
                                                hidden_layer_dropout, input_layer_dropout, dropout_rate,
                                                kernel_regularizer))
                                            results.append(
                                                "验证集结果：%s，优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s，正则化：%s" % (
                                                train_DNN(X_train, y_train, X_test, y_test,
                                                          optimizer=optimizer,
                                                          hidden_layer_num=hidden_layer_num,
                                                          hidden_layer_units=hidden_layer_units,
                                                          batch_size=batch_size,
                                                          hidden_layer_dropout=hidden_layer_dropout,
                                                          input_layer_dropout=input_layer_dropout,
                                                          dropout_rate=dropout_rate,
                                                          use_kernel_regularizer=use_kernel_regularizer,
                                                          kernel_regularizer=kernel_regularizer), optimizer,
                                                hidden_layer_num, hidden_layer_units, batch_size, hidden_layer_dropout,
                                                input_layer_dropout, dropout_rate, kernel_regularizer))
                                    else:
                                        print(
                                            "优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s，正则化：%s" % (
                                            optimizer, hidden_layer_num, hidden_layer_units, batch_size,
                                            hidden_layer_dropout, input_layer_dropout, dropout_rate,
                                            kernel_regularizer))
                                        results.append(
                                            "验证集结果：%s，优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s" % (
                                            train_DNN(X_train, y_train, X_test, y_test,
                                                      optimizer=optimizer,
                                                      hidden_layer_num=hidden_layer_num,
                                                      hidden_layer_units=hidden_layer_units,
                                                      batch_size=batch_size,
                                                      hidden_layer_dropout=hidden_layer_dropout,
                                                      input_layer_dropout=input_layer_dropout,
                                                      dropout_rate=dropout_rate), optimizer, hidden_layer_num,
                                            hidden_layer_units, batch_size, hidden_layer_dropout, input_layer_dropout,
                                            dropout_rate))
                        else:
                            if use_kernel_regularizer == True:
                                for kernel_regularizer in kernel_regularizer_list:
                                    print("优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，正则化：%s" % (
                                    optimizer, hidden_layer_num, hidden_layer_units, batch_size, hidden_layer_dropout,
                                    input_layer_dropout, kernel_regularizer))
                                    results.append(
                                        "验证集结果：%s，优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s，正则化：%s" % (
                                        train_DNN(X_train, y_train, X_test, y_test,
                                                  optimizer=optimizer,
                                                  hidden_layer_num=hidden_layer_num,
                                                  hidden_layer_units=hidden_layer_units,
                                                  batch_size=batch_size,
                                                  use_kernel_regularizer=use_kernel_regularizer,
                                                  kernel_regularizer=kernel_regularizer), optimizer, hidden_layer_num,
                                        hidden_layer_units, batch_size, kernel_regularizer))
                            else:
                                print("优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s" % (
                                optimizer, hidden_layer_num, hidden_layer_units, batch_size, hidden_layer_dropout,
                                input_layer_dropout))
                                results.append(
                                    "验证集结果：%s，优化器：%s，隐层数量：%s，隐层单元数：%s，bacth大小：%s，隐层dropout：%s，输入层dropout：%s，dropout_rate：%s" % (
                                    train_DNN(X_train, y_train, X_test, y_test,
                                              optimizer=optimizer,
                                              hidden_layer_num=hidden_layer_num,
                                              hidden_layer_units=hidden_layer_units,
                                              batch_size=batch_size), optimizer, hidden_layer_num, hidden_layer_units,
                                    batch_size, hidden_layer_dropout, input_layer_dropout))


